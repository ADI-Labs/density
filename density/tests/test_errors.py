import json
import conftest

def test_bad_date(app, auth_header):
    resp = app.get("/day/23/group/85", headers=auth_header)
    body = json.loads(resp.data)

    assert resp.status_code == 400
    assert "error" in body
    assert "YYYY-MM-DD" in body["error"]

def test_good_date(app, auth_header):
    resp = app.get("/day/2014-10-23/group/85", headers=auth_header)
    body = json.loads(resp.data)

    assert resp.status_code == 200
    assert len(body["data"]) == 96
