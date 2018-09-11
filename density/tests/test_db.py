import datetime as dt

from freezegun import freeze_time
import pytest
import pytz

from density import db


def test_bad_insert(cursor):
    cursor.execute("SELECT MAX(dump_time) FROM density_data")
    previous = cursor.fetchone()["max"]

    data = {"150": {"name": "Wrong", "client_count": "0", "parent_id": "84"}}
    with pytest.raises(KeyError):
        db.insert_density_data(cursor, data)

    data = {"102": {"name": "Wrong", "client_count": "0", "parent_id": "101"}}
    with pytest.raises(RuntimeError):
        db.insert_density_data(cursor, data)

    cursor.execute("SELECT MAX(dump_time) FROM density_data")
    assert previous == cursor.fetchone()["max"]


def test_good_insert(cursor):
    data = {
        "155": {
            "parent_id": "153",
            "name": "John Jay Dining Hall",
            "client_count": "140",
        },
        "192": {
            "parent_id": "153",
            "name": "JJ's Place",
            "client_count": "83",
        },
        "117": {
            "parent_id": "115",
            "name": "Butler Library 3",
            "client_count": "250",
        },
        "116": {
            "parent_id": "115",
            "name": "Butler Library 2",
            "client_count": "336",
        },
        "111": {
            "parent_id": "109",
            "name": "Lehman Library 3",
            "client_count": "150",
        },
        "110": {
            "parent_id": "109",
            "name": "Lehman Library 2",
            "client_count": "43",
        },
        "119": {
            "parent_id": "115",
            "name": "Butler Library 4",
            "client_count": "168",
        },
        "118": {
            "parent_id": "117",
            "name": "Butler Library 301",
            "client_count": "236",
        },
        "96": {
            "parent_id": "2",
            "name": "Uris/Watson Library",
            "client_count": "223",
        },
        "120": {
            "parent_id": "115",
            "name": "Butler Library 5",
            "client_count": "62",
        },
        "98": {
            "parent_id": "97",
            "name": "Starr East Asian Library",
            "client_count": "90",
        },
        "122": {
            "parent_id": "115",
            "name": "Butler Library stk",
            "client_count": "50",
        },
        "125": {
            "parent_id": "124",
            "name": "Architectural and Fine Arts Library 1",
            "client_count": "2",
        },
        "126": {
            "parent_id": "124",
            "name": "Architectural and Fine Arts Library 2",
            "client_count": "61",
        },
        "127": {
            "parent_id": "124",
            "name": "Architectural and Fine Arts Library 3",
            "client_count": "66",
        },
        "102": {"parent_id": "101", "name": "Lerner 1", "client_count": "85"},
        "103": {"parent_id": "101", "name": "Lerner 2", "client_count": "0"},
        "100": {
            "parent_id": "99",
            "name": "Science and Engineering Library",
            "client_count": "65",
        },
        "106": {"parent_id": "101", "name": "Lerner 5", "client_count": "0"},
        "107": {
            "parent_id": "101",
            "name": "Roone Arledge Auditorium",
            "client_count": "0",
        },
        "104": {"parent_id": "101", "name": "Lerner 3", "client_count": "86"},
        "105": {"parent_id": "101", "name": "Lerner 4", "client_count": "0"},
        "121": {
            "parent_id": "115",
            "name": "Butler Library 6",
            "client_count": "90",
        },
    }

    date = dt.datetime(2017, 5, 5).astimezone(pytz.timezone("US/Eastern"))
    with freeze_time(date.astimezone(pytz.utc)):
        db.insert_density_data(cursor, data)

    cursor.execute("SELECT MAX(dump_time) FROM density_data")
    assert cursor.fetchone()["max"] == date.replace(tzinfo=None)

    cursor.execute("""
    DELETE FROM density_data
        WHERE dump_time = (SELECT MAX(dump_time) FROM density_data)
    ;""")
