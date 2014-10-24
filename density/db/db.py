import psycopg2


TABLE_NAME = 'density'


def get_latest_row(cursor):
    query = "SELECT * FROM {name} ORDER BY timestamp DESC, " \
            "LIMIT 1".format(TABLE_NAME)
    cursor.execute(query)
    result = cursor.fetch_one()
    return result