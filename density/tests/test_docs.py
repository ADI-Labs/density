import json

def test_docs(app, auth_header):
    resp = app.get("/docs", headers=auth_header)

    assert resp.status_code == 200

def test_building_info(app, auth_header):
    resp = app.get("/docs/building_info", headers=auth_header)
    body = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(body['data']) == 23

    for row in body["data"]:
        assert row.keys() == {'group_id',
                              'group_name', 'parent_id', 'parent_name'}
