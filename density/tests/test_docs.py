import copy
import json

import density


def test_docs(app, auth_header):
    resp = app.get("/docs", headers=auth_header)

    assert resp.status_code == 200
