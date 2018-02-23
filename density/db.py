import base64
import datetime as dt
import os
import uuid

import pytz

SELECT = """
    SELECT d.client_count, d.dump_time,
           r.id AS group_id, r.name AS group_name,
           b.id AS parent_id, b.name AS building_name
    FROM density_data d
    JOIN routers r ON r.id = d.group_id
    JOIN buildings b ON b.id = r.building_id"""

QUERY_LIMIT = 100


def get_latest_data(cursor):
    """
    Gets the latest data for all group ids.

    :param cursor: cursor for our DB
    :return: list of dicts representing each row from the db
    :rtype: list of dict
    """
    query = SELECT + """
        WHERE d.dump_time = (SELECT MAX(dump_time) FROM density_data)
        ORDER BY group_name
    ;"""
    cursor.execute(query)
    print("fetch called")
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

    query = SELECT + """
        WHERE d.dump_time = (SELECT MAX(dump_time) FROM density_data)
              AND group_id = %s
    ;"""
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

    query = SELECT + """
        WHERE d.dump_time = (SELECT MAX(dump_time) FROM density_data)
              AND building_id = %s
    ;"""
    cursor.execute(query, [parent_id])
    return cursor.fetchall()


def get_window_based_on_group(cursor, group_id, start_time, end_time, offset):
    """
    Gets all data for a group within a window. It will return the latest 100
    rows starting with the most recent ones.

    :param cursor: cursor for our DB
    :param int group_id: id of the group requested
    :param str start_time: start time of window
    :param str end_time: end time of the window
    :param int offset: how much to offset the query by
    :return: list of dictionaries representing the rows corresponding to the
    query
    :rtype: list of dict
    """
    query = SELECT + """
        WHERE d.dump_time >= %s AND
              d.dump_time < %s AND
              group_id = %s
        ORDER BY d.dump_time DESC
        LIMIT %s OFFSET %s
    ;"""
    cursor.execute(query,
                   [start_time, end_time, group_id, QUERY_LIMIT, offset])
    return cursor.fetchall()


def get_window_based_on_parent(cursor, parent_id, start_time, end_time,
                               offset):
    """
    Gets all data for a parent id (building) within a window. It will return
    the latest rows starting with the most recent ones.

    :param cursor: cursor for our DB
    :param int parent_id: id of the group requested
    :param str start_time: start time of window
    :param str end_time: end time of the window
    :param int offset: how much to offset the query by
    :return: list of dictionaries representing the rows corresponding to the
    query
    :rtype: list of dict
    """

    query = SELECT + """
        WHERE d.dump_time >= %s AND
              d.dump_time < %s AND
              building_id=%s
        ORDER BY d.dump_time DESC
        LIMIT %s OFFSET %s
    ;"""
    cursor.execute(query,
                   [start_time, end_time, parent_id, QUERY_LIMIT, offset])
    return cursor.fetchall()


def get_building_info(cursor):
    """
    Gets names and ids for groups and parents

    :param cursor:
    """
    query = """
        SELECT r.name AS group_name, r.id AS group_id,
               b.name AS parent_name, b.id AS parent_id
        FROM routers r
        JOIN buildings b ON r.building_id = b.id
        ORDER BY parent_name, group_name;
    """
    cursor.execute(query)
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
               WHERE uni=%s LIMIT 1;"""
    cursor.execute(query, [uni])
    result = cursor.fetchone()

    if result is not None:
        return result['code']
    else:
        # If the code DNE, create a new one and insert into the database.
        token_bytes = os.urandom(32) + uuid.uuid4().bytes
        new_code = base64.urlsafe_b64encode(token_bytes).decode()
        query = """INSERT INTO oauth_data (uni, code)
                   VALUES (%s, %s);"""
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
               WHERE code=%s LIMIT 1;"""
    cursor.execute(query, [code])
    result = cursor.fetchone()
    if result is not None:
        return result['uni']


def insert_density_data(cursor, data):
    # Check integrity of data
    cursor.execute("""
    SELECT name, id, building_id AS parent_id
    FROM routers r
    ;""")
    groups = {row["id"]: row for row in cursor.fetchall()}

    rows = []

    time = (dt.datetime.now(tz=pytz.utc)
            .astimezone(pytz.timezone("US/Eastern"))
            .replace(tzinfo=None))  # drop timezone info for Postgres

    for key, value in data.items():
        group = {
            "id": int(key),
            "name": value["name"],
            "parent_id": int(value["parent_id"])
        }
        client_count = int(value["client_count"])

        # Data normalization issue on CUIT's side
        if group["parent_id"] == 131 and group["name"] == "Butler Library 301":
            group["parent_id"] = 103

        if groups[group["id"]] != group:
            raise RuntimeError(f"Invalid group found: {group}")

        rows.append([time, group["id"], client_count])

    query = """
    INSERT INTO density_data
        (dump_time, group_id, client_count)
        VALUES (%s, %s, %s)
    ;"""
    cursor.executemany(query, rows)
