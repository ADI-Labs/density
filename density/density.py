from flask import Flask, g, jsonify

app = Flask(__name__)
# do import early to check that all env variables are present
app.config.from_object('config.flask_config')

# library imports
import psycopg2
import psycopg2.pool
import psycopg2.extras
from datetime import datetime

<<<<<<< HEAD
=======

>>>>>>> Created db module and get_latest_data function
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
    g.start_time = datetime.now()


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
    with open('static/index.html') as f:
        return f.read()


@app.route('/latest')
def get_latest_data():
    """
    Gets latest dump of data for all endpoints.

    :return: Latest JSON
    :rtype: flask.Response
    """

    # create fakeData for testing
    fakeData = [{"dump_time": "9999-12-31 23:59:59",
                 "group_id": 152,
                 "group_name": "Lerner 3",
                 "parent_id": "84",
                 "parent_name": "Lerner",
                 "client_count": "70"},
                {"dump_time": '0000-01-01 00:00:00',
                 "group_id": 131,
                 "group_name": "Butler Library 3",
                 "parent_id": 103,
                 "parent_name": "Butler",
                 "client_count": 328}]

    return jsonify(data=fakeData)


@app.route('/latest/group/<group_id>')
def get_latest_group_data(group_id):
    """
    Gets latest dump of data for the specified group.

    :param int group_id: id of the group requested
    :return: Latest JSON corresponding to the requested group
    :rtype: flask.Response
    """
    return group_id


@app.route('/latest/building/<building_id>')
def get_latest_building_data(building_id):
    """
    Gets latest dump of data for the specified building.

    :param int building_id: id of the building requested
    :return: Latest JSON corresponding to the requested building
    :rtype: flask.Response
    """
    return building_id


@app.route('/day/<day>/group/<group_id>')
def get_day_group_data(day, group_id):
    """
    Gets specified group data for specified day

    :param str day: the day requested in ET format YYYY-MM-DD
    :param int group_id: id of the group requested
    :return: JSON corresponding to the requested day and group
    :rtype: flask.Response
    """
    return day + " " + group_id


@app.route('/day/<day>/building/<building_id>')
def get_day_building_data(day, building_id):
    """
    Gets specified building data for specified day

    :param str day: the day requested in ET format YYYY-MM-DD
    :param int building_id: id of the building requested
    :return: JSON corresponding to the requested day and building
    :rtype: flask.Response
    """
    return day + " " + building_id


@app.route('/window/<start_time>/<end_time>/group/<group_id>')
def get_window_group_data(start_time, end_time, group_id):
    """
    Gets specified group data split by the specified time delimiter.

    :param str start_time: start time in ET format YYYY-MM-DDThh:mm
    :param str end_time: end time in ET format YYYY-MM-DDThh:mm
    :param int group_id: id of the group requested
    :return: JSON corresponding to the requested window and group
    :rtype: flask.Response
    """
    return start_time + " " + end_time + " " + group_id


@app.route('/window/<start_time>/<end_time>/building/<building_id>')
def get_window_building_data(start_time, end_time, building_id):
    """
    Gets specified building data split by the specified time delimiter.

    :param str start_time: start time in ET format YYYY-MM-DDThh:mm
    :param str end_time: end time in ET format YYYY-MM-DDThh:mm
    :param int building_id: id of the building requested
    :return: JSON corresponding to the requested window and building
    :rtype: flask.Response
    """
    return start_time + " " + end_time + " " + building_id


if __name__ == '__main__':
    app.run(host=app.config['HOST'])
