import json

import density


def test_latest_data(app, auth_header):
    resp = app.get("/latest", headers=auth_header)
    body = json.loads(resp.data)

    assert resp.status_code == 200
    assert len(body["data"]) == 22                   # check # of responses
    assert 2 == len([room for room in body["data"]   # check # of empty rooms
                     if not room["client_count"]])


def test_annotate_fullness_percentage():
    cur_data = [{
        "client_count": 5,
        "dump_time": "Sat, 01 Nov 2014 19:45:00 GMT",
        "group_id": 147,
        "group_name": "Architectural and Fine Arts Library 1",
        "parent_id": 146,
        "parent_name": "Avery"
    }]
    # Extract capacity of lib from FULL_CAP_DATA
    AFALibrary1_capacity = 0
    for cap in density.FULL_CAP_DATA:
        if cap['group_id'] == 147:
            AFALibrary1_capacity = cap['capacity']
            break
    result_percent = 5.0 / AFALibrary1_capacity * 100
    result_data = [{
        "client_count": 5,
        "dump_time": "Sat, 01 Nov 2014 19:45:00 GMT",
        "group_id": 147,
        "group_name": "Architectural and Fine Arts Library 1",
        "parent_id": 146,
        "parent_name": "Avery",
        "percent_full": result_percent
    }]

    assert density.annotate_fullness_percentage(cur_data) == result_data
