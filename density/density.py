from flask import Flask, g, jsonify, render_template, json

app = Flask(__name__)
# do import early to check that all env variables are present
app.config.from_object('config.flask_config')

# library imports
import psycopg2
import psycopg2.pool
import psycopg2.extras
import datetime
import db.db as db


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
    return_connections()
    # TODO: log the request and its outcome
    return resp


@app.route('/')
def home():
    return render_template('index.html')


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
    # TODO: Authenticate user and return page based on whether authentication
    # was successful
    return render_template('auth.html')


@app.route('/latest')
def get_latest_data():
    """
    Gets latest dump of data for all endpoints.

    :return: Latest JSON
    :rtype: flask.Response
    """

    fetched_data = db.get_latest_data(g.cursor)

    return jsonify(data=fetched_data)


@app.route('/latest/group/<group_id>')
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


@app.route('/capacity')
def capacity():
    """Render and show capacity page """

    # Read capacity of groups from json file
    json_data = open('data/capacity_group.json')
    cap_data = json.load(json_data)['data']
    # Read current data
    cur_data = db.get_latest_data(g.cursor)
    locations = []

    # Loop to find corresponding cur_client_count with capacity
    # and store it in locations
    for cap in cap_data:

        groupName = cap['group_name']
        capacity = cap['capacity']

        for latest in cur_data:
            if latest['group_name'] == groupName:
                cur_client_count = latest['client_count']
                break
        # Cast one of the numbers into a float, get a percentile by multiplying
        # 100, round the percentage and cast it back into a int.
        percent_full = int(round(float(cur_client_count)/capacity*100))
        locations.append({"name": groupName, "fullness": percent_full})

    return render_template('capacity.html', locations=locations)


if __name__ == '__main__':
    app.run(host=app.config['HOST'])
