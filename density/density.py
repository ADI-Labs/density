from __future__ import print_function

from functools import wraps
import copy
import datetime
import httplib2
import re
import traceback

from bokeh.embed import components
from flask import Flask, g, jsonify, render_template, json, request
from flask_mail import Message, Mail
import psycopg2
import psycopg2.pool
import psycopg2.extras
from oauth2client.client import flow_from_clientsecrets

from db import db
from config import flask_config

from data import sample_out


app = Flask(__name__)
app.config.update(**flask_config.config)
if not app.debug:
    mail = Mail(app)

# change the default JSON encoder to handle datetime's properly
app.json_encoder = flask_config.ISO8601Encoder

with open('data/capacity_group.json') as json_data:
    FULL_CAP_DATA = json.load(json_data)['data']

CU_EMAIL_REGEX = r"^(?P<uni>[a-z\d]+)@.*(columbia|barnard)\.edu$"
request_date_format = '%Y-%m-%d'

# create a pool of postgres connections
pg_pool = psycopg2.pool.SimpleConnectionPool(
    5,      # min connections
    20,     # max connections
    database=app.config['PG_DB'],
    user=app.config['PG_USER'],
    password=app.config['PG_PASSWORD'],
    host=app.config['PG_HOST'],
    port=app.config['PG_PORT'],
)


@app.before_request
def get_connections():
    """ Get connections from the Postgres pool. """
    g.pg_conn = pg_pool.getconn()
    g.cursor = g.pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    g.start_time = datetime.datetime.now()


def return_connections():
    """ Return the connection to the Postgres connection pool. """
    g.cursor.close()
    pg_pool.putconn(g.pg_conn)


def unsafe_date(*keys):
    """ Takes URL parameters to filter as an argument """
    def dec(fn):
        @wraps(fn)
        def validate_datetime(*args, **kwargs):
            for dt in keys:
                arg_date = request.view_args.get(dt)
                try:
                    datetime.datetime.strptime(arg_date, request_date_format)
                except ValueError:
                    return jsonify(error=("Invalid datetime format, "
                                          "'{}', please use YYYY-MM-DD format")
                                   .format(arg_date)), 400

            return fn(*args, **kwargs)
        return validate_datetime
    return dec


@app.after_request
def log_outcome(resp):
    """ Outputs to a specified logging file """
    # return db connections first
    g.pg_conn.commit()
    return_connections()
    # TODO: log the request and its outcome
    return resp


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
@app.errorhandler(Exception)
def internal_error(e):
    if not app.debug:
        msg = Message("DENSITY ERROR", sender="densitylogger@gmail.com",
                      recipients=app.config['ADMINS'])
        msg.body = traceback.format_exc()
        mail.send(msg)
    return jsonify(error="Something went wrong, and notification of "
                   "admins failed.  Please contact an admin.",
                   error_data=traceback.format_exc())
    # return jsonify(error="Something went wrong, the admins were notified.")


def authorization_required(func):
    @wraps(func)
    def authorization_checker(*args, **kwargs):
        token = request.headers.get('Authorization-Token')
        if not token:
            token = request.args.get('auth_token')
            if not token:
                response = jsonify(error="No authorization token provided")
                response.status_code = 401      # unauthorized
                return response

        uni = db.get_uni_for_code(g.cursor, token)
        if not uni:
            response = jsonify(error="No authorization token provided")
            response.status_code = 401          # unauthorized
            return response

        # TODO: Some logging right here. We can log which user is using what.
        return func(*args, **kwargs)
    return authorization_checker


def annotate_fullness_percentage(cur_data):
    """
    Calculates percent fullness of all groups and adds them to the data in
    the key 'percent_full'. The original data file is not modified.
    :param list of dictionaries cur_data: data to calculate fullness percentage
    :return: list of dictionaries with added pecent_full data
    :rtype: list of dictionaries
    """

    # copy so that original list is not affected
    cur_data_copy = copy.copy(cur_data)

    for data in cur_data_copy:

        group_name = data['group_name']
        cur_client_count = data['client_count']

        for cap in FULL_CAP_DATA:
            if cap['group_name'] == group_name:
                capacity = cap['capacity']
                break

        # Percent full in float
        if capacity:
            percent_full = float(cur_client_count) / capacity * 100
            data["percent_full"] = percent_full
        else:
            data["percent_full"] = None

    # Match percentage and group by order of list
    return cur_data_copy


@app.route('/home')
def home():
    return render_template('index.html',
                           client_id=app.config['GOOGLE_CLIENT_ID'])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict')
def predict():
    locations = sorted(group["group_name"] for group in FULL_CAP_DATA)
    plot = {l: sample_out() for l in locations}

    script,div = components(plot)
    return render_template('predict_layout.html', script=script,div=div)


@app.route('/docs')
def docs():
    return render_template('docs.html')


@app.route('/docs/building_info')
def building_info():
    """
    Gets a json with the group ids, group names, parent ids, and parent names
    """

    fetched_data = db.get_building_info(g.cursor)

    return jsonify(data=fetched_data)


@app.route('/auth')
def auth():
    """
    Returns an auth code after user logs in through Google+.
    :param string code: code that is passed in through Google+.
                        Do not provide this yourself.
    :return: An html page with an auth code.
    :rtype: flask.Response
    """

    # Get code from params.
    code = request.args.get('code')
    if not code:
        return render_template('auth.html',
                               success=False)

    try:
        # Exchange code for email address.
        # Get Google+ ID.
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        gplus_id = credentials.id_token['sub']

        # Get first email address from Google+ ID.
        http = httplib2.Http()
        http = credentials.authorize(http)

        h, content = http.request(
            'https://www.googleapis.com/plus/v1/people/' + gplus_id, 'GET')
        data = json.loads(content)
        email = data["emails"][0]["value"]

        # Verify email is valid.
        regex = re.match(CU_EMAIL_REGEX, email)

        if not regex:
            return render_template('auth.html',
                                   success=False,
                                   reason="Please log in with your " +
                                   "Columbia or Barnard email. You logged " +
                                   "in with: " + email)

        # Get UNI and ask database for code.
        uni = regex.group('uni')
        code = db.get_oauth_code_for_uni(g.cursor, uni)
        return render_template('auth.html', success=True, uni=uni, code=code)
    except Exception as e:
        # TODO: log errors
        print(e)
        return render_template('auth.html',
                               success=False,
                               reason="An error occurred. Please try again.")


@app.route('/latest')
@authorization_required
def get_latest_data():
    """
    Gets latest dump of data for all endpoints.
    :return: Latest JSON
    :rtype: flask.Response
    """

    fetched_data = db.get_latest_data(g.cursor)

    # Add percentage_full
    fetched_data = annotate_fullness_percentage(fetched_data)

    return jsonify(data=fetched_data)


@app.route('/latest/group/<group_id>')
@authorization_required
def get_latest_group_data(group_id):
    """
    Gets latest dump of data for the specified group.
    :param int group_id: id of the group requested
    :return: Latest JSON corresponding to the requested group
    :rtype: flask.Response
    """

    fetched_data = db.get_latest_group_data(g.cursor, group_id)

    # Add percentage_full
    fetched_data = annotate_fullness_percentage(fetched_data)

    return jsonify(data=fetched_data)


@app.route('/latest/building/<parent_id>')
@authorization_required
def get_latest_building_data(parent_id):
    """
    Gets latest dump of data for the specified building.
    :param int parent_id: id of the building requested
    :return: Latest JSON corresponding to the requested building
    :rtype: flask.Response
    """

    fetched_data = db.get_latest_building_data(g.cursor, parent_id)

    # Add percentage_full
    fetched_data = annotate_fullness_percentage(fetched_data)

    return jsonify(data=fetched_data)


@app.route('/day/<day>/group/<group_id>')
@unsafe_date('day')
@authorization_required
def get_day_group_data(day, group_id):
    """
    Gets specified group data for specified day
    :param str day: the day requested in EST format YYYY-MM-DD
    :param int group_id: id of the group requested
    :return: JSON corresponding to the requested day and group
    :rtype: flask.Response
    """

    # Convert to datetime object
    start_day = datetime.datetime.strptime(day, "%Y-%m-%d")
    end_day = start_day + datetime.timedelta(days=1)

    fetched_data = db.get_window_based_on_group(g.cursor, group_id, start_day,
                                                end_day, offset=0)
    # Add percentage_full
    fetched_data = annotate_fullness_percentage(fetched_data)

    return jsonify(data=fetched_data)


@app.route('/day/<day>/building/<parent_id>')
@unsafe_date('day')
@authorization_required
def get_day_building_data(day, parent_id):
    """
    Gets specified building data for specified day
    :param str day: the day requested in EST format YYYY-MM-DD
    :param int parent_id: id of the building requested
    :return: JSON corresponding to the requested day and building
    :rtype: flask.Response
    """

    # Convert to datetime object
    start_day = datetime.datetime.strptime(day, "%Y-%m-%d")
    end_day = start_day + datetime.timedelta(days=1)

    fetched_data = db.get_window_based_on_parent(g.cursor, parent_id,
                                                 start_day, end_day, offset=0)

    # Add percentage_full
    fetched_data = annotate_fullness_percentage(fetched_data)

    return jsonify(data=fetched_data)


@app.route('/window/<start_time>/<end_time>/group/<group_id>')
@authorization_required
def get_window_group_data(start_time, end_time, group_id):
    """
    Gets specified group data split by the specified time delimiter.
    :param str start_time: start time in EST format YYYY-MM-DDThh:mm
    :param str end_time: end time in EST format YYYY-MM-DDThh:mm
    :param int group_id: id of the group requested
    :return: JSON corresponding to the requested window and group
    :rtype: flask.Response
    """
    offset = request.args.get('offset', type=int) if request.args.get(
        'offset') else 0
    fetched_data = db.get_window_based_on_group(g.cursor, group_id, start_time,
                                                end_time, offset)
    # Add percentage_full
    fetched_data = annotate_fullness_percentage(fetched_data)

    next_page_url = None
    if len(fetched_data) == db.QUERY_LIMIT:
        new_offset = offset + db.QUERY_LIMIT
        next_page_url = request.base_url + '?auth_token=' + request.args.get(
            'auth_token') + '&offset=' + str(new_offset)

    return jsonify(data=fetched_data, next_page=next_page_url)


@app.route('/window/<start_time>/<end_time>/building/<parent_id>')
@authorization_required
def get_window_building_data(start_time, end_time, parent_id):
    """
    Gets specified building data split by the specified time delimiter.
    :param str start_time: start time in EST format YYYY-MM-DDThh:mm
    :param str end_time: end time in EST format YYYY-MM-DDThh:mm
    :param int parent_id: id of the building requested
    :return: JSON corresponding to the requested window and building
    :rtype: flask.Response
    """
    offset = request.args.get('offset', type=int) if request.args.get(
        'offset') else 0
    fetched_data = db.get_window_based_on_parent(g.cursor, parent_id,
                                                 start_time, end_time, offset)
    # Add percentage_full
    fetched_data = annotate_fullness_percentage(fetched_data)

    next_page_url = None
    if len(fetched_data) == db.QUERY_LIMIT:
        new_offset = offset + db.QUERY_LIMIT
        next_page_url = request.base_url + '?auth_token=' + request.args.get(
            'auth_token') + '&offset=' + str(new_offset)
    return jsonify(data=fetched_data, next_page=next_page_url)


@app.route('/capacity/group')
def get_cap_group():
    """
    Return capacity of all groups.
    :return: List of dictionaries having keys "group_name", "capacity",
    "group_id"
    :rtype: List of dictionaries
    """

    fetched_data = db.get_cap_group(g.cursor)

    return jsonify(data=fetched_data)


@app.route('/')
def capacity():
    """ Render and show capacity page """
    normfmt = '%B %d %Y, %I:%M %p'
    cur_data = db.get_latest_data(g.cursor)
    last_updated = cur_data[0]['dump_time']
    last_updated = last_updated.strftime(normfmt)
    locations = calculate_capacity(FULL_CAP_DATA, cur_data)
    return render_template('capacity.html', locations=locations,
                           last_updated=last_updated)


def calculate_capacity(cap_data, cur_data):
    """
    Calculates capacity with cap_data and cur_data and puts
    with respective group_name into locations
    """

    locations = []

    # Loop to find corresponding cur_client_count with capacity
    # and store it in locations
    for cap in cap_data:

        group_name = cap['group_name']
        capacity = cap['capacity']
        parentId = cap['parent_id']
        parentName = cap['parent_name']

        for latest in cur_data:
            if latest['group_name'] == group_name:
                cur_client_count = latest['client_count']
                break
        # Cast one of the numbers into a float, get a percentile by multiplying
        # 100, round the percentage and cast it back into a int.
        percent_full = int(round(float(cur_client_count) / capacity * 100))
        if percent_full > 100:
            percent_full = 100

        if group_name == 'Butler Library stk':
            group_name = 'Butler Library Stacks'
        elif group_name == 'Science and Engineering Library':
            group_name = 'NoCo Library'

        locations.append({"name": group_name, "fullness": percent_full,
                          "parentId": parentId, "parentName": parentName})
    return locations


@app.route('/map')
def map():
    """ Render and show maps page """

    cur_data = db.get_latest_data(g.cursor)

    locations = calculate_capacity(FULL_CAP_DATA, cur_data)
    # Render template has an SVG image whose colors are changed by % full
    return render_template('map.html', locations=locations)

if __name__ == '__main__':
    app.run(host=app.config['HOST'])
