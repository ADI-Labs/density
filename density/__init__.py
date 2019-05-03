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
import pytz

from . import librarytimes, locationauxdata
from . import db
from . import graphics
from .config import config, ISO8601Encoder
from .data import FULL_CAP_DATA, resize_full_cap_data, COMBINATIONS

from .predict import categorize_data, get_db_queries, predict_from_dataframes

from .locationauxdata import LOCATION_AUX_DATA
from apscheduler.schedulers.background import BackgroundScheduler
import exponent_server_sdk as push_notification
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

app = Flask(__name__)

CU_EMAIL_REGEX = r"^(?P<uni>[a-z\d]+)@.*(columbia|barnard)\.edu$"

# multiply each building's max capcity by this
PERCENTAGE_FULL_CAP_DATA = 0.9

REQUEST_DATE_FORMAT = '%Y-%m-%d'

# Cache deletes elements after this many seconds
CACHE_DEFAULT_TIMEOUT_SECONDS = 8*24*60*60

# Cache Predictions data for this many days
CACHE_PREDICTIONS_DATA_DAYS = 7

# max number of weeks to go back and forward to get clusters in predictions algorithm
MAX_WEEK_DELTA_PREDICTIONS = 1

# number of seconds for BackgroundScheduler to wait to call cache_prediction_data() 
INTERVAL_CACHE_PREDICTION_DATA = 10

# create a pool of postgres connections
# ThreadedConnectionPool may be used in several threads, as occurs in cache_prediction_data()
pg_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=5, maxconn=20, dsn=config["DB_URI"])


# Create a cache to store Bokeh prediction graphs
# and prediction graphs raw data. Every element is
# deleted after CACHE_DEFAULT_TIMEOUT_SECONDS
server_cache = SimpleCache(default_timeout=CACHE_DEFAULT_TIMEOUT_SECONDS)
print("Cache initialized with default_timeout: " + str(CACHE_DEFAULT_TIMEOUT_SECONDS))

# FULL_CAP_DATA each value changed to PERCENTAGE_FULL_CAP_DATA * value
err_msg = resize_full_cap_data(PERCENTAGE_FULL_CAP_DATA)
if(err_msg != "0"):
    print("resize_full_cap_data() failed and returned: " + err_msg)


# initialize BackgroundScheduler
apsched = BackgroundScheduler()
apsched.start()
print("BackgroundScheduler initialized")

def cache_prediction_data(days=CACHE_PREDICTIONS_DATA_DAYS):
    """
        Called by apscheduler to cache predictions' Bokeh data and raw data
        Runs in a separate thread
        All error checking needs to be done inside function since it is called from a BackgroundScheduler
        :param int days: number of days to cache predictions data for
        :return: int error_code: -1: error , 0: no error
    """

    # Run the function using the flask app_context
    # so the app scheduler process still uses the same postgres pool (pg_pool) as the parent process
    with app.app_context():

        """
        PostgreSQL's timestamp: Sunday = 0, Saturday = 6, 
        First week = 1 if it has more than 3 days, First week = 0 if it has less than 3 days 
        Python's datetime.weekday(): Monday = 0, Sunday = 6, 
        datetime.isocalendar()[1]: First week = 1 if it has more than 3 days 
        """
        date = datetime.datetime.now(pytz.timezone('US/Eastern'))

        week_of_year = date.isocalendar()[1]
        day_of_week = date.weekday()

        # Adjust day_of_week from (Monday = 0, Sunday = 6) to (Sunday = 0, Saturday = 6)
        if (day_of_week + 1 == 7):
            day_of_week = 0
        else:
            day_of_week = day_of_week + 1

        if(week_of_year > 53 or week_of_year < 0):
            print("ERROR: week_of_year is not between 0-53. week_of_year = "+str(week_of_year))
            print("Aborting predictions calculation... No data in cache was changed")
            return -1

        if(day_of_week > 6 or day_of_week < 0):
            print("ERROR: day_of_week is not between 0-6. day_of_week = "+str(day_of_week))
            print("Aborting predictions calculation... No data in cache was changed")
            return -1

        print(".....................................................................")

        print(".....................................................................")
        print("Caching prediction Bokeh graphs for the next "+str(days)+" days")
        print("day_of_week (Sunday = 0, Saturday = 6): " + str(day_of_week))
        print("week_of_year: " + str(week_of_year))
        print("MAX_WEEK_DELTA_PREDICTIONS: "+ str(MAX_WEEK_DELTA_PREDICTIONS))
        print("\nThis will take a while.........")
        
        #handle pool connection
        g.pg_conn = pg_pool.getconn()
        g.cursor = g.pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        g.start_time = datetime.datetime.now() 

        # int arrays date.weekday() combinations, each int is day_of_week to combine in cluster

        combinations_day_of_week = COMBINATIONS[date.weekday()]
        if not combinations_day_of_week:
            print("ERROR COMBINATIONS[date.weekday()] is empty. date.weekday(): "+ str(date.weekday()))
            combinations_day_of_week = COMBINATIONS[0] # default - Monday
            print("combinations_day_of_week set to "+str(combinations_day_of_week))

        print("Trying clusters... "+str(combinations_day_of_week))

        print("For "+str(MAX_WEEK_DELTA_PREDICTIONS)+" weeks back and forward")
        print("Total clusters: "+str(MAX_WEEK_DELTA_PREDICTIONS*MAX_WEEK_DELTA_PREDICTIONS*len(combinations_day_of_week)))
 
        # to store all queries to execute in categorize_data
        queries = get_db_queries(day_of_week, week_of_year, MAX_WEEK_DELTA_PREDICTIONS, combinations_day_of_week)
        

        # default in case queries is empty
        if not queries:
            query = ' WHERE extract(WEEK from d.dump_time) = ' + \
                                '{} AND extract(DOW from d.dump_time) = '.format(week_of_year) + \
                                '{}'.format(day_of_week)
            queries = [query]

        
        print("Number of queries prepared to fetch: "+str(len(queries)))
        print("Fetching data from queries........")

        # to store pandas.core.frame.DataFrame returned by categorize_data()
        dataframes = []

        for query in queries:
            data = categorize_data(g.cursor, query)
            if(type(data) == 'str'):
                print(data)
            else:
                dataframes.append(data)

        print("Successfully fetched "+str(len(dataframes))+" queries and converted to pandas dataframes")

        if not dataframes:
            print("ERROR: No pandas DataFrame returned by categorize_data() for any query")
            print("Aborting predictions calculation... No data in cache was changed")
            return -1

        #print(dataframes)
        # make predictions using all clusters
        today_pred = predict_from_dataframes(dataframes)
        if(type(today_pred) == "str"):
            print("ERROR: predict_from_dataframes() returned error: ")
            print(today_pred)
            print("Aborting predictions calculation... No data in cache was changed")
            return -1

        # returns script and divs with all graphs for one day, to be cached
        script, divs = graphics.create_all_buildings(today_pred.transpose())
        script = script.replace('<script type="text/javascript">', "").replace('</script>', "")
        print("HELLOOOOOOOPOPOPOOOOOO")
        print(today_pred)
        server_cache.set('monday_script', script, timeout=0)
        server_cache.set('monday_div', divs, timeout=0)
        server_cache.set('today_pred', today_pred, timeout=0)

    return 0


def check_percent_diff():
    """
    Calculates difference in percent fullness between the prediction and live data
    of all groups and adds them to the data in the key 'percent_diff'. The original 
    data is not modified.
    """
    data = annotate_fullness_percentage(db.get_latest_data(g.cursor))
    pred = annotate_fullness_percentage(server_cache.get('today_pred'))
    data_with_diffs = []
    for row in data:
        copy = dict(**row)
        this_percent = row["percent_full"]
        predicted_percent = 0
        for group in pred:
            if group["group_name"] == row["group_name"]:
                predicted_percent = group["percent_full"]
        copy["percent_diff"] = abs(this_percent - predicted_percent)
        data_with_diffs.append(copy)
    return data_with_diffs


# add job to cache predictions Bokeh and raw data every week
apsched.add_job(cache_prediction_data, 'interval', seconds=INTERVAL_CACHE_PREDICTION_DATA, max_instances=1)
print("Added job to BackgroundScheduler: cache_prediction_data() every "+str(INTERVAL_CACHE_PREDICTION_DATA)+" seconds")

# When we deploy to server, we need to call 
# home page once so it will load predictions' data onto server's cache
# TODO: poor solution - resolve this by rendering 404 not found if not loaded yet

@app.before_first_request
def initialize():
    """
        Loads predictions' Bokeh and raw data onto cache and initializes BackgroundScheduler
        Runs right before processing the first request made to Flask app
        TODO: Load predictions' raw data onto cache
    """
    # done first so we can handle those predictions' requests
    err_msg = cache_prediction_data(CACHE_PREDICTIONS_DATA_DAYS)
    # if(err_msg != "0"):
    #     print("cache_prediction_data failed and returned: " + err_msg)




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
                    datetime.datetime.strptime(arg_date, REQUEST_DATE_FORMAT)
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

       #Temporarily commented out to test API Calls in the local environment
       #Need to uncomment before deployment.
        """
        uni = db.get_uni_for_code(g.cursor, token)
        if not uni:
            response = jsonify(error="No authorization token provided")
            response.status_code = 401  # unauthorized
            return response
        """

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
    Modified to output open/closing time for all the buildings
    """
    fetched_data = db.get_latest_data(g.cursor)

    # Add percentage_full
    fetched_data = annotate_fullness_percentage(fetched_data)

    #Dictionary containing opening/closing time for all buildings
    open_close_data = librarytimes.dict_for_time()
    #Iterates through each building, adding open_close_time key with the
    #appropriate value from open_close_data
    for val in fetched_data:
        val['open_close_time'] = open_close_data[val['group_name']]
        val['location_type'] = LOCATION_AUX_DATA[val['group_name']]['type']
        val['nickname'] = LOCATION_AUX_DATA[val['group_name']]['nickname']
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

def find_all(a_str, sub):
    print("sub")
    print(sub)
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

@app.route('/predict')
def predict():
    today = datetime.datetime.today().weekday() + 1
    if today > 6:
        today = 0
    today = 0
    auxdata = locationauxdata.get_location_aux_data()
    times = librarytimes.dict_for_time()

    divs = []
    divs.append(server_cache.get('monday_div'))
    divs.append(server_cache.get('tuesday_div'))
    for elem in divs:
        for location_name, d in divs[today].items():
            divs[today][location_name] = divs[today][location_name][1:]

        today = today + 1

    today = 0
    script = []
    script.append(server_cache.get('monday_script'))
    script.append(server_cache.get('tuesday_script'))


    return render_template('predict.html', divs=divs,
                           script=script, css_script=CDN.render_js(),
                           times=times, auxdata=auxdata, today=today)

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



@app.route('/feedback/<group_id>/<feedback_percentage>/<current_percentage>', methods =['POST'])
def upload_feedback(group_id, feedback_percentage, current_percentage):
    #May not need this variable
    #current_devices = db.get_latest_building_data(g.cursor, building_id)
    updated_percentage = int(current_percentage )+ int(feedback_percentage);
    group_id = int(group_id)
    try:
        db.insert_updated_data_to_feedback_table(g.cursor, group_id, updated_percentage)
    except Exception as e:
        print (e)
        return 'Invalid insertion of user feedback'

    return 'User feedback successfully uploaded.', 200

@app.route('/users/signup', methods = ['GET', 'POST'])
def register_user():
    #Gets user email data from the App and posts it to the database
    #Needs to have the dump.sql file with new user_data table in it to test it locally
    data = request.get_json()
    dataDict = dict(data)
    """
    Assumes json format =
    {
      "email" : "xxx@columbia.edu",
      "favorite_dininghall" : "John Jay",
      "favorite_library" : "Butler 3"
     }
    """
    user_email = dataDict["email"]
    fav_dininghall = dataDict["favorite_dininghall"]
    fav_library = dataDict["favorite_library"]

    #register_success = False
    #update_dininghall_success = False
    #update_library_success = False

    try:
        db.insert_user_email(g.cursor, user_email)
        #register_success = True
    except Exception as e:
        print (e)
        return 'Failed to register a new user'

    try:
        db.update_fav_dininghall(g.cursor, user_email, fav_dininghall)
        #update_dininghall_success = True
    except Exception as e:
        print (e)
        return 'Failed to set favorite dininghall'

    try:
        db.update_fav_library(g.cursor, user_email, fav_library)
        #update_library_success = True
    except Exception as e:
        print (e)
        return 'Failed to set favorite dininghall'

    #if register_success and update_dininghall_success and update_library_success:
    return 'Successfully registered user with preferences', 200
    #else:
        #return 'User registration unsuccessful', 200

#API endpoint for registering push notification token unique to each user
@app.route('/users/push-token', methods = ['GET', 'POST'])
def register_user_token():
    data = request.get_json()
    dataDict = dict(data)
    token = dataDict["token"]
    user_email = dataDict["user_email"]
    #token_register_success = False

    try:
        db.update_token(g.cursor, user_email, token)
        #token_register_success = True
    except Exception as e:
        print (e)
        return 'Failed to add notification token for the user'

    #if token_register_success:
    #    return 'Successfully registered notification token for the user', 200
    #else:
    return 'Successfully registered notification token for the user', 200

#Function to send a push notification containing message to a device corresponding
#to the token.
def send_push_message(token, message, extra=None):
    try:
        response = push_notification.PushClient().publish(
            push_notification.PushMessage(to=token,
                        body=message,
                        data=extra))
    except push_notification.PushServerError as exc:
        # Encountered some likely formatting/validation error.
        rollbar.report_exc_info(
            extra_data={
                'token': token,
                'message': message,
                'extra': extra,
                'errors': exc.errors,
                'response_data': exc.response_data,
            })
        raise
    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        rollbar.report_exc_info(
            extra_data={'token': token, 'message': message, 'extra': extra})
        raise self.retry(exc=exc)

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except push_notification.DeviceNotRegisteredError:
        # Mark the push token as inactive
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
    except push_notification.PushResponseError as exc:
        # Encountered some other per-notification error.
        rollbar.report_exc_info(
            extra_data={
                'token': token,
                'message': message,
                'extra': extra,
                'push_response': exc.push_response._asdict(),
            })
        raise self.retry(exc=exc)
