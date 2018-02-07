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
        

def test_latest_group_data(app, auth_header):
    resp = app.get("/latest/group/148", headers=auth_header)
    body = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(body["data"]) == 1
    assert body["data"][0]["building_name"] == "Avery"
    assert body["data"][0]["group_name"] == (
        "Architectural and Fine Arts Library 2")
    assert body["data"][0]["parent_id"] == 146
    assert body["data"][0]["group_id"] == 148
        

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
