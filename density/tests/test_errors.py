import json

def test_bad_date(app, auth_header):
    resp = app.get("/day/23/group/85", headers=auth_header)
    body = json.loads(resp.data.decode())

    assert resp.status_code == 400
    assert "error" in body
    assert "YYYY-MM-DD" in body["error"]

def test_good_date(app, auth_header):
    resp = app.get("/day/2014-10-21/group/85", headers=auth_header)
    body = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(body["data"]) == 17

def test_no_auth(app):
    resp = app.get("/day/2014-10-21/group/85")
    body = json.loads(resp.data.decode())

    assert "No authorization token" in body["error"]
    assert resp.status_code == 401      # unauthorized

def test_bad_auth(app):
    resp = app.get("/day/2014-10-21/group/85",
                   headers={"Authorization-Token": "fake auth token"})
    body = json.loads(resp.data.decode())

    assert "No authorization token" in body["error"]
