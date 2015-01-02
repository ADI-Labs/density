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

    :param cursor: cursor for our DB
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

def get_cap_group(cursor):
    """
    Gets the max capacity of all groups. Equation for max capacity is average +
    std*2. We're estimating the 95th percentile as average + std*2.

    :param cursor: cursor for our DB
    :return: list of dictionaries representing the rows corresponding to the
    query
    :rtype: list of dict
    """

    query = """SELECT cast(
                          max(client_count)
                          as int
                       )  as capacity, group_id, group_name
               FROM {table_name}
               GROUP BY group_name, group_id
               ORDER BY group_name
               ;""".format(table_name=TABLE_NAME)
    cursor.execute(query)
    return cursor.fetchall()

def get_building_info(cursor):
    """
    Gets names and ids for groups and parents

    :param cursor:
    """
    query = """SELECT DISTINCT
                 group_name, group_id, parent_name, parent_id
                 FROM {table_name}
                 ORDER BY parent_name, group_name;
                 ;""".format(table_name=TABLE_NAME)
    cursor.execute(query)
    return cursor.fetchall()
