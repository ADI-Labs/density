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

def migrate_dump_time(cursor):
    query = SELECT+";"
    cursor.execute(query)
    while True:
        r = cursor.fetchone()
        if(r == None):
            break
        if(r['dump_time'].minute is not 0 and r['dump_time'].minute is not 15 and r['dump_time'].minute is not 30 and r['dump_time'].minute is not 45):
            print(r['dump_time'].minute)

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

    # TODO: do a schema migration to make this data normalization moot
    parent_ids = {
        101: 84,        # Lerner
        109: 79,        # Lehman Library
        115: 103,       # Butler
        117: 103,       # Butler 301
        124: 146,       # Avery
        153: 75,        # John Jay
        2: 2,           # Uris,
        97: 62,         # East Asian Library
        99: 15,         # NoCo
    }
    ids = {
        100: 145,      # Science and Engineering Library
        102: 150,      # Lerner 1
        103: 151,      # Lerner 2
        104: 152,      # Lerner 3
        105: 153,      # Lerner 4
        106: 154,      # Lerner 5
        107: 85,       # Roone Arledge Auditorium
        110: 139,      # Lehman Library 2
        111: 140,      # Lehman Library 3
        116: 130,      # Butler Library 2
        117: 131,      # Butler Library 3
        118: 171,      # Butler Library 301
        119: 132,      # Butler Library 4
        120: 133,      # Butler Library 5
        121: 134,      # Butler Library 6
        122: 138,      # Butler Library stk
        125: 147,      # Architectural and Fine Arts Library 1
        126: 148,      # Architectural and Fine Arts Library 2
        127: 149,      # Architectural and Fine Arts Library 3
        155: 125,      # John Jay Dining Hall
        192: 155,      # JJ's Place
        96: 23,        # Uris/Watson Library
        98: 144,       # Starr East Asian Library
    }

    for key, value in data.items():
        group = {
            "id": ids[int(key)],
            "name": value["name"],
            "parent_id": parent_ids[int(value["parent_id"])]
        }
        client_count = int(value["client_count"])
        if groups[group["id"]] != group:
            raise RuntimeError(f"Invalid group found: {group}")

        rows.append([time, group["id"], client_count])

    query = """
    INSERT INTO density_data
        (dump_time, group_id, client_count)
        VALUES (%s, %s, %s)
    ;"""
    cursor.executemany(query, rows)

def insert_updated_data_to_feedback_table(cursor, group_id, updated_percentage):
    # to get the raw_count currently displaying to user
    data = get_latest_group_data(cursor, group_id)
    raw_count = data[0]['client_count']

    query = "INSERT INTO feedback_data (group_id, raw_count, percentage_change) VALUES ("+str(group_id)+","+str(raw_count)+","+str(updated_percentage)+");"
    cursor.execute(query)

    return "Sucess"

def insert_user_email(cursor, email):
    """
    adds a new user as a row in user_data table
    :param str email: User email from /signup endpoint
    """
    query = "INSERT INTO user_data (user_email, fav_dininghall, fav_library) VALUES (%s, NULL, NULL);"
    cursor.execute(query, [email])
    return "Success"

def update_fav_dininghall(cursor, email, dininghall):
    """
    updates user's favorite dininghall
    :param str email: User email from /signup endpoint
    :param str dininghall: User's favorite dininghall from /signup endpoint
    """

    query = "UPDATE user_data SET fav_dininghall = %s WHERE user_email = %s;"
    cursor.execute(query, [dininghall, email])
    return "Success"

def update_fav_library(cursor, email, library):
    """
    updates user's favorite library
    :param str email: User email from /signup endpoint
    :param str library: User's favorite library from /signup endpoint
    """

    query = "UPDATE user_data SET fav_library = %s WHERE user_email = %s;"
    cursor.execute(query, [library, email])
    return "Success"

def update_token(cursor, email, token):
    """
    updates user's notification token
    :param str email: User email from /signup endpoint
    :param str token: From mobile app LogInScreen.js
    """

    query = "UPDATE user_data SET token = %s WHERE user_email = %s;"
    cursor.execute(query, [token, email])
    return "Success"
