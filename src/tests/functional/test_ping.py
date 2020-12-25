# src/tests/test_ping.py

import json


# USE Given - When - Then testing framework
def test_ping(test_app):
    # given, ie state of application before test
    client = test_app.test_client()
    # when, ie behaviour being tested
    resp = client.get("/ping")
    data = json.loads(resp.data.decode())
    # then, ie changes based on behaviour (asserts)
    assert resp.status_code == 200
    assert "pong" in data["message"]
    assert "success" in data["status"]
