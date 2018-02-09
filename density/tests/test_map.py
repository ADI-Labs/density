def test_map(app, auth_header):
    resp = app.get("/map", headers=auth_header)

    assert resp.status_code == 200
