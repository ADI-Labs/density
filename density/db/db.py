import psycopg2


TABLE_NAME = 'density_data'
QUERY_LIMIT = 100


def get_latest_data(cursor):
    """
    Gets the latest data for all group ids.

    :param cursor: cursor for our DB
    :return: list of dicts representing each row from the db
    :rtype: list of dict
    """
    query = """SELECT * FROM {table_name} WHERE dump_time=(SELECT MAX("
             "dump_time) FROM {table_name});""".format(table_name=TABLE_NAME)
    cursor.execute(query)
    return cursor.fetchall()


def get_window_based_on_group(cursor, group_id, start_time, end_time):
    """
    Gets all data for a group within a window. It will return the latest 100
    rows starting with the most recent ones.

    :param cursor:
    :param int group_id: id of the group requested
    :param str start_time: start time of window
    :param str end_time: end time of the window
    :return: list of dictionaries representing the rows corresponding to the
    query
    :rtype: list of dict
    """
    query = """SELECT * FROM {}
               WHERE (dump_time >= %s
                      AND dump_time <= %s)
                      AND group_id=%s
               LIMIT %s
               ORDER BY dump_time DESC;""".format(TABLE_NAME)
    cursor.execute(query, [start_time, end_time, group_id,
                   QUERY_LIMIT])
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
    query = """SELECT * FROM {}
               WHERE (dump_time >= %s
                      AND dump_time <= %s)
                      AND parent_id=%s
               LIMIT %s
               ORDER BY dump_time DESC;""".format(TABLE_NAME)
    cursor.execute(query, [start_time, end_time, parent_id,
                   QUERY_LIMIT])
    return cursor.fetchall()
