import psycopg2


TABLE_NAME = 'density'


def get_latest_data(cursor):
    """
    Gets the latest data for all group ids.

    :param cursor: cursor for our DB
    :return: list of dicts representing each row from the db
    :rtype: list of dict
    """
    query = "SELECT * FROM %s WHERE dump_time=(SELECT MAX(" \
            "dump_time) FROM %s);"
    cursor.execute(query, TABLE_NAME, TABLE_NAME)
    return cursor.fetchall()
