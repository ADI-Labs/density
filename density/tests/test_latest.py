import copy
import json

import density


def test_latest_data(app, auth_header):
    resp = app.get("/latest", headers=auth_header)
    body = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(body["data"]) == 22                   # check # of responses
    for row in body["data"]:
        assert row.keys() == {'client_count', 'building_name', 'client_count',
                              'dump_time', 'group_name', 'group_id',
                              'percent_full', 'parent_id'}

def test_annotate_fullness_percentage():
    data = [{
        "client_count": 5,
        "dump_time": "Sat, 01 Nov 2014 19:45:00 GMT",
        "group_id": 147,
        "group_name": "Architectural and Fine Arts Library 1",
        "parent_id": 146,
        "parent_name": "Avery"
    }]

    original = copy.deepcopy(data)
    annotated = density.annotate_fullness_percentage(data)

    assert original == data     # did not edit original

    data[0]["percent_full"] = 22
    assert annotated == data

def test_window_group_data():
    group_id = 144
    start_time, end_time = '2014-10-21 19:45:00', '2014-10-21 20:15:00'

