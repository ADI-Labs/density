import psycopg2
import random
import string


TABLE_NAME = 'density_data'
QUERY_LIMIT = 100


def get_latest_data(cursor):
    """
    Gets the latest data for all group ids.

    :param cursor: cursor for our DB
    :return: list of dicts representing each row from the db
    :rtype: list of dict
    """
    query = """SELECT *
               FROM {table_name}
               WHERE dump_time=(
                   SELECT MAX(dump_time)
                   FROM {table_name}
               )
               ;""".format(table_name=TABLE_NAME)
    cursor.execute(query)
    return cursor.fetchall()


def get_latest_group_data(cursor, group_id):
    """
    Gets latest dump of data for the specified group.

    :param cursor: cursor for our DB
    :param int group_id: id of the requested group
    :return:  list of dictionaries representing the rows corresponding to the
    query
    :rtype: list of dict
    """

    query = """SELECT *
               FROM {table_name}
               WHERE dump_time=(
                   SELECT MAX(dump_time)
                   FROM {table_name}
               ) AND group_id=%s
               ;""".format(table_name=TABLE_NAME)
    cursor.execute(query, [group_id])
    return cursor.fetchall()


def get_latest_building_data(cursor, parent_id):
    """
    Gets latest dump of data for the specified building.

    :param cursor: cursor for our DB
    :param int parent_id: id of the requested building
    :return:  list of dictionaries representing the rows corresponding to the
    query
    :rtype: list of dict
    """

    query = """SELECT *
               FROM {table_name}
               WHERE dump_time=(
                   SELECT MAX(dump_time)
                   FROM {table_name}
               ) AND parent_id=%s
               ;""".format(table_name=TABLE_NAME)
    cursor.execute(query, [parent_id])
    return cursor.fetchall()


def get_window_based_on_group(cursor, group_id, start_time, end_time):
    """
    Gets all data for a group within a window. It will return the latest 100
    rows starting with the most recent ones.

    :param cursor: cursor for our DB
    :param int group_id: id of the group requested
    :param str start_time: start time of window
    :param str end_time: end time of the window
    :return: list of dictionaries representing the rows corresponding to the
    query
    :rtype: list of dict
    """
    query = """SELECT *
               FROM {table_name}
               WHERE (
                    dump_time >= %s
                    AND dump_time <= %s
               ) AND group_id=%s
               ORDER BY dump_time DESC
               LIMIT %s
               ;""".format(table_name=TABLE_NAME)
    cursor.execute(query, [start_time, end_time, group_id, QUERY_LIMIT])
    return cursor.fetchall()


def get_window_based_on_parent(cursor, parent_id, start_time, end_time):
    """
    Gets all data for a parent id (building) within a window. It will return
    the latest rows starting with the most recent ones.

    :param cursor:
    :param int parent_id: id of the group requested
    :param str start_time: start time of window
    :param str end_time: end time of the window
    :return: list of dictionaries representing the rows corresponding to the
    query
    :rtype: list of dict
    """
    query = """SELECT *
               FROM {table_name}
               WHERE (
                    dump_time >= %s
                    AND dump_time <= %s
               ) AND parent_id=%s
               ORDER BY dump_time DESC
               LIMIT %s
               ;""".format(table_name=TABLE_NAME)
    cursor.execute(query, [start_time, end_time, parent_id, QUERY_LIMIT])
    return cursor.fetchall()


def get_oauth_code_for_uni(cursor, uni):
    """
    :param str uni: UNI
    :return: code for the user (generates new code if doesn't exist)
    :rtype: str
    """
    # Try getting the code from the database.
    query = """SELECT code
               FROM oauth_data
               WHERE uni=%s;"""
    cursor.execute(query, [uni])
    results = cursor.fetchall()

    if results:
      return results[0]['code']
    else:
      # If the code doesn't exist, create a new one and insert into the database.
      new_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
      query = """INSERT INTO oauth_data (uni, code) VALUES (%s, %s);"""
      cursor.execute(query, [uni, new_code])
      return new_code


def get_uni_for_code(cursor, code):
    """
    :param str code: oauth code
    :return: the uni for the user, or None if oauth code doesn't exist
    :rtype: str
    """
    query = """SELECT uni
               FROM oauth_data
               WHERE code=%s;"""
    cursor.execute(query, [code])
    results = cursor.fetchall()
    if results:
      return results[0]['uni']
    else:
      return None
