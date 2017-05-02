import datetime as dt

from freezegun import freeze_time
import pytest

from density import db


def test_bad_insert(cursor):
    cursor.execute("SELECT MAX(dump_time) FROM density_data")
    previous = cursor.fetchone()["max"]

    data = {"150": {"name": "Wrong", "client_count": "0", "parent_id": "84"}}
    with pytest.raises(RuntimeError):
        db.insert_density_data(cursor, data)

    cursor.execute("SELECT MAX(dump_time) FROM density_data")
    assert previous == cursor.fetchone()["max"]


@freeze_time("2017-01-01")
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

    db.insert_density_data(cursor, data)

    cursor.execute("SELECT MAX(dump_time) FROM density_data")
    assert cursor.fetchone()["max"] == dt.datetime(2017, 1, 1)

    cursor.execute("""
    DELETE FROM density_data
        WHERE dump_time = (SELECT MAX(dump_time) FROM density_data)
    ;""")
