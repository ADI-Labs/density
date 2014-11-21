from flask import Flask, g, jsonify, render_template, request

app = Flask(__name__)
# do import early to check that all env variables are present
app.config.from_object('config.flask_config')

# library imports
import psycopg2
import psycopg2.pool
import psycopg2.extras
import datetime
from oauth2client.client import flow_from_clientsecrets
import httplib2
import json
from db import db
import re
from functools import wraps

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


@app.after_request
def log_outcome(resp):
    """ Outputs to a specified logging file """
    # return db connections first
    g.pg_conn.commit()
    return_connections()
    # TODO: log the request and its outcome
    return resp


def authorization_required(func):
    @wraps(func)
    def authorization_checker(*args, **kwargs):
        token = request.headers.get('Authorization-Token')
        if not token:
            return jsonify(data={"error": "No authorization token provided."})

        uni = db.get_uni_for_code(g.cursor, token)
        if not uni:
            return jsonify(data={"error": "Invalid authorization token."})

        # TODO: Some logging right here. We can log which user is using what.
        return func(*args, **kwargs)
    return authorization_checker


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/docs')
def docs():
    return render_template('docs.html')


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
                               success=False,
                               reason="You need to log in!")

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

        h, content = http.request('https://www.googleapis.com/plus/v1/people/'
                                  + gplus_id, 'GET')
        data = json.loads(content)
        email = data["emails"][0]["value"]

        # Verify email is valid.
        regex = re.match("^(?P<uni>[\w_\d]+)@(columbia|barnard)\.edu$", email)

        if not regex:
            return render_template('auth.html',
                                   success=False,
                                   reason="You need to log in with your"
                                   + "Columbia or Barnard email! You logged "
                                   + "in with: "
                                   + email)

        # Get UNI and ask database for code.
        uni = regex.group('uni')
        code = db.get_oauth_code_for_uni(g.cursor, uni)
        return render_template('auth.html', success=True, uni=uni, code=code)
    except:
        return render_template('auth.html',
                               success=False,
                               reason="An error occurred. Please try again"
                               + "later.")


@app.route('/latest')
@authorization_required
def get_latest_data():
    """
    Gets latest dump of data for all endpoints.

    :return: Latest JSON
    :rtype: flask.Response
    """

    fetched_data = db.get_latest_data(g.cursor)

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

    return jsonify(data=fetched_data)


@app.route('/day/<day>/group/<group_id>')
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
    end_day = start_day + datetime.timedelta(1)

    fetched_data = db.get_window_based_on_group(g.cursor, group_id, start_day,
                                                end_day)

    return jsonify(data=fetched_data)


@app.route('/day/<day>/building/<parent_id>')
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
    end_day = start_day + datetime.timedelta(1)

    fetched_data = db.get_window_based_on_parent(g.cursor, parent_id,
                                                 start_day, end_day)

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

    fetched_data = db.get_window_based_on_group(g.cursor, group_id, start_time,
                                                end_time)

    return jsonify(data=fetched_data)


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

    fetched_data = db.get_window_based_on_parent(g.cursor, parent_id,
                                                 start_time, end_time)

    return jsonify(data=fetched_data)


if __name__ == '__main__':
    app.run(host=app.config['HOST'])
