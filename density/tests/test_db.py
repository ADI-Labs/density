import datetime as dt

from freezegun import freeze_time
import pytest
import pytz

from density import db


def test_bad_insert(cursor):
    cursor.execute("SELECT MAX(dump_time) FROM density_data")
    previous = cursor.fetchone()["max"]

    data = {"150": {"name": "Wrong", "client_count": "0", "parent_id": "84"}}
    with pytest.raises(RuntimeError):
        db.insert_density_data(cursor, data)

    cursor.execute("SELECT MAX(dump_time) FROM density_data")
    assert previous == cursor.fetchone()["max"]


def test_good_insert(cursor):
    data = {
        "171": {
            "name": "Butler Library 301",
            "client_count": "69",
            "parent_id": "131"
        },
        "150": {
            "name": "Lerner 1",
            "client_count": "1",
            "parent_id": "84"
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
