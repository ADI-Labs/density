import datetime
from functools import wraps
import json
import re
import traceback

from bokeh.resources import CDN
from flask import Flask, g, jsonify, render_template, request
import httplib2
from oauth2client.client import flow_from_clientsecrets
import psycopg2
import psycopg2.extras
import psycopg2.pool
from werkzeug.contrib.cache import SimpleCache

from . import db, librarytimes, locationauxdata
from . import graphics
from .config import config, ISO8601Encoder
from .data import FULL_CAP_DATA
from .predict import categorize_data, multi_predict
from .predict import db_to_pandas, predict_today
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

CU_EMAIL_REGEX = r"^(?P<uni>[a-z\d]+)@.*(columbia|barnard)\.edu$"
request_date_format = '%Y-%m-%d'

# create a pool of postgres connections
pg_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=5, maxconn=20, dsn=config["DB_URI"])


def sample_test():
    with app.app_context():
        g.pg_conn = pg_pool.getconn()
        g.cursor = g.pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        g.start_time = datetime.datetime.now() 
    
        print("This is a test of apscheduler")
        for i in range(1,8):
            date = datetime.datetime.today()
            date += datetime.timedelta(days=i)
            data = categorize_data(g.cursor, 0, date)
            data1 = categorize_data(g.cursor, 1, date)
            data2 = categorize_data(g.cursor, 2, date)
            data3 = categorize_data(g.cursor, 3, date)
            data4 = categorize_data(g.cursor, 4, date)
            data5 = categorize_data(g.cursor, 5, date)
            data6 = categorize_data(g.cursor, 6, date)

        # make predictions using all clusters
            today_pred = multi_predict(data, data1, data2,
                                         data3, data4, data5, data6)

        # display data
            #print(today_pred)
            script, divs = graphics.create_all_buildings(today_pred.transpose())
            if (i == 1):
                predictionCache.set('monday_script', script, timeout=0)
                predictionCache.set('monday_div', divs, timeout=0)
            if (i == 2):
                predictionCache.set('tuesday_script', script, timeout=0)
                predictionCache.set('tuesday_div', divs, timeout=0)
            if (i == 3):
                predictionCache.set('wednesday_script', script, timeout=0)
                predictionCache.set('wednesday_div', divs, timeout=0)
            if (i == 4):
                predictionCache.set('thursday_script', script, timeout=0)
                predictionCache.set('thursday_div', divs, timeout=0)
            if (i == 5):
                predictionCache.set('friday_script', script, timeout=0)
                predictionCache.set('friday_div', divs, timeout=0)
            if (i == 6):
                predictionCache.set('saturday_script', script, timeout=0)
                predictionCache.set('saturday_div', divs, timeout=0)
            if (i == 7):
                predictionCache.set('sunday_script', script, timeout=0)
                predictionCache.set('sunday_div', divs, timeout=0)

@app.before_first_request
def initialize():
    sample_test()
    apsched = BackgroundScheduler()
    apsched.start()
    apsched.add_job(sample_test,  'interval', seconds=10)


@app.before_request
def get_connections():
    """ Get connections from the Postgres pool. """
    g.pg_conn = pg_pool.getconn()
    g.cursor = g.pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    g.start_time = datetime.datetime.now()
    
    

cache = SimpleCache()
predictionCache = SimpleCache()
# app.scheduler = BackgroundScheduler()
# job = app.scheduler.add_job(sample_test, 'interval', seconds=10)
# app.scheduler.start()
    # within this block, current_app points to app.
    




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
                    return jsonify(
                        error=("Invalid datetime format, "
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


if not app.debug:

    @app.errorhandler(500)
    @app.errorhandler(Exception)
    def internal_error(e):
        traceback.print_exc()
        return jsonify(
            error="Something went wrong, and notification of "
            "admins failed.  Please contact an admin.",
            error_data=traceback.format_exc())


def authorization_required(func):
    @wraps(func)
    def authorization_checker(*args, **kwargs):
        token = request.headers.get('Authorization-Token')
        if not token:
            token = request.args.get('auth_token')
            if not token:
                response = jsonify(error="No authorization token provided")
                response.status_code = 401  # unauthorized
                return response

        uni = db.get_uni_for_code(g.cursor, token)
        if not uni:
            response = jsonify(error="No authorization token provided")
            response.status_code = 401  # unauthorized
            return response

        # TODO: Some logging right here. We can log which user is using what.
        return func(*args, **kwargs)

    return authorization_checker


def annotate_fullness_percentage(data):
    """
    Calculates percent fullness of all groups and adds them to the data in
    the key 'percent_full'. The original data is not modified.
    :param list of dictionaries cur_data: data to calculate fullness percentage
    :return: list of dictionaries with added pecent_full data
    :rtype: list of dictionaries
    """
    groups = []
    for row in data:
        capacity = FULL_CAP_DATA[row["group_name"]]
        percent = (100 * row["client_count"]) // capacity

        copy = dict(**row)
        copy["percent_full"] = min(100, percent)
        groups.append(copy)
    return groups


@app.route('/about')
def about():
    return render_template('about.html')


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
    print(code)
    if not code:
        return render_template('auth.html', success=False)

    try:
        # Exchange code for email address.
        # Get Google+ ID.
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        print(oauth_flow)
        print("trying")
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        print(credentials)
        gplus_id = credentials.id_token['sub']
        print(gplus_id)

        # Get first email address from Google+ ID.
        http = httplib2.Http()
        http = credentials.authorize(http)

        h, content = http.request(
            'https://www.googleapis.com/plus/v1/people/' + gplus_id, 'GET')
        data = json.loads(content)
        print(data)
        email = data["emails"][0]["value"]

        # Verify email is valid.
        regex = re.match(CU_EMAIL_REGEX, email)

        if not regex:
            return render_template(
                'auth.html',
                success=False,
                reason="Please log in with your " +
                "Columbia or Barnard email. You logged " + "in with: " + email)

        # Get UNI and ask database for code.
        uni = regex.group('uni')
        code = db.get_oauth_code_for_uni(g.cursor, uni)
        return render_template('auth.html', success=True, uni=uni, code=code)
    except psycopg2.IntegrityError:
        return render_template(
            'auth.html',
            success=False,
            reason="Attempt to generate API key resulted in"
            " a collision with another key in the"
            " database. Please refresh to try and"
            " generate a new key.")

    except Exception as e:
        # TODO: log errors
        print(e)
        return render_template(
            'auth.html',
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

    fetched_data = db.get_window_based_on_group(
        g.cursor, group_id, start_day, end_day, offset=0)
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

    fetched_data = db.get_window_based_on_parent(
        g.cursor, parent_id, start_day, end_day, offset=0)

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
    offset = request.args.get(
        'offset', type=int) if request.args.get('offset') else 0
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
    offset = request.args.get(
        'offset', type=int) if request.args.get('offset') else 0
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


@app.route('/')
def capacity():
    """Render and show capacity page"""
    cur_data = db.get_latest_data(g.cursor)
    last_updated = cur_data[0]['dump_time'].strftime("%B %d %Y, %I:%M %p")
    locations = annotate_fullness_percentage(cur_data)
    auxdata = locationauxdata.get_location_aux_data()
    # times = {'Lerner 1' : 1200, 'Lerner 2' : 1300}
    times = librarytimes.dict_for_time()
    return render_template(
        'capacity.html', locations=locations,
        last_updated=last_updated, times=times, auxdata=auxdata, today='hi')


@app.route('/map')
def map():
    cur_data = db.get_latest_data(g.cursor)
    locations = annotate_fullness_percentage(cur_data)

    # Render template has an SVG image whose colors are changed by % full
    return render_template('map.html', locations=locations)

@app.route('/new_predict')
def new_predict():

    today = datetime.datetime.today().weekday() + 1
    if today > 6:
        today = 0
    auxdata = locationauxdata.get_location_aux_data()
    times = librarytimes.dict_for_time()
    # for i in range(1,8):
    #     date = datetime.datetime.today()
    #     date += datetime.timedelta(days=i)
    #     data = categorize_data(g.cursor, 0, date)
    #     data1 = categorize_data(g.cursor, 1, date)
    #     data2 = categorize_data(g.cursor, 2, date)
    #     data3 = categorize_data(g.cursor, 3, date)
    #     data4 = categorize_data(g.cursor, 4, date)
    #     data5 = categorize_data(g.cursor, 5, date)
    #     data6 = categorize_data(g.cursor, 6, date)

    # # make predictions using all clusters
    #     today_pred = multi_predict(data, data1, data2,
    #                                  data3, data4, data5, data6)

    # # display data
    #     print(today_pred)
    #     script, divs = graphics.create_all_buildings(today_pred.transpose())
    #     if (i == 1):
    #         predictionCache.set('monday_script', script, timeout=0)
    #         predictionCache.set('monday_div', divs, timeout=0)
    #     if (i == 2):
    #         predictionCache.set('tuesday_script', script, timeout=0)
    #         predictionCache.set('tuesday_div', divs, timeout=0)
    #     if (i == 3):
    #         predictionCache.set('wednesday_script', script, timeout=0)
    #         predictionCache.set('wednesday_div', divs, timeout=0)
    #     if (i == 4):
    #         predictionCache.set('thursday_script', script, timeout=0)
    #         predictionCache.set('thursday_div', divs, timeout=0)
    #     if (i == 5):
    #         predictionCache.set('friday_script', script, timeout=0)
    #         predictionCache.set('friday_div', divs, timeout=0)
    #     if (i == 6):
    #         predictionCache.set('saturday_script', script, timeout=0)
    #         predictionCache.set('saturday_div', divs, timeout=0)
    #     if (i == 7):
    #         predictionCache.set('sunday_script', script, timeout=0)
    #         predictionCache.set('sunday_div', divs, timeout=0)
            
    divs = [predictionCache.get('sunday_div'), predictionCache.get('monday_div'), predictionCache.get('tuesday_div'), predictionCache.get('wednesday_div'), predictionCache.get('thursday_div'), predictionCache.get('friday_div'), predictionCache.get('saturday_div')]
    script = [predictionCache.get('sunday_script'), predictionCache.get('monday_script'), predictionCache.get('tuesday_script'), predictionCache.get('wednesday_script'), predictionCache.get('thursday_script'), predictionCache.get('friday_script'), predictionCache.get('saturday_script')]

    return render_template('predict.html', divs=json.dumps(divs),
                           script=script, css_script=CDN.render_js(),
                           times=times, auxdata=auxdata, today=today)


@app.route('/predict')
def predict():
    auxdata = locationauxdata.get_location_aux_data()
    times = librarytimes.dict_for_time()
    # loading data from current database connection
    data = cache.get('predictData')

    if data is None:
        data = db_to_pandas(g.cursor)
        cache.set('predictData', data, timeout=10600)

    # make predictions based on fetched data

    today_pred = cache.get('predictToday')

    if today_pred is None:
        today_pred = predict_today(data)
        cache.set('predictToday', today_pred, timeout=10600)

    # make plots from predictions
    print(today_pred)
    script = cache.get('predictScript')
    divs = cache.get('predictDivs')
    print(today_pred.transpose().head())
    if script is None:
        script, divs = graphics.create_all_buildings(today_pred.transpose())
        cache.set('predictScript', script, timeout=10600)
        cache.set('predictDivs', divs, timeout=10600)
    '''
    data = db_to_pandas(g.cursor)
    today_pred = predict_today(data)
    script, divs = graphics.create_all_buildings(today_pred.transpose())
    '''
    
    return render_template('predict.html', divs=divs,
                           script=script, css_script=CDN.render_js(),
                           times=times, auxdata=auxdata)


@app.route('/upload', methods=['POST'])
def upload():
    """ Accept POST requests from CUIT to add new data to the server """
    # This is stored in local settings and is the way we verify uploads.
    if request.args.get('key') != config['UPLOAD_KEY']:
        return 'Please include a valid API key.', 401

    try:
        db.insert_density_data(g.cursor, request.get_json())
    except Exception as e:
        # TODO: proper logging
        print(e)
        return 'At least one of the records was not inserted. \
            Please contact someone in ADI for more details.', 500

    return 'Data successfully uploaded.', 200

"""
@app.route('/feedback/<building_id>/<feedack_percentage>/<current_percentage>', methods =['POST'])
def upload_feedback(building_id, feedback_percentage, current_percentage):
    #May not need this variable
    current_devices = db.get_latest_building_data(g.cursor, building_id)
    updated_percentage = current_percentage * (100 / (100 - feedback_percentage))
    try:
        db.insert_updated_data_to_feedback_table(g.cursor, building_id, updated_percentage)
    except Exception as e:
        print (e)
        return 'Invalid insertion of user feedback'

    return 'User feedback successfully uploaded.', 200
"""
