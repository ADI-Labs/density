import json

def test_about(app):
	resp = app.get('/');
	assert resp.status_code == 200