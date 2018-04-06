def test_about(app):
    resp = app.get('/about')
    assert resp.status_code == 200
