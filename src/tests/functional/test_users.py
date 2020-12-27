# src/tests/functional/test_users

# list of HTTP status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

import json

from src.api.models import User


# POST route
def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"username": "dataandgis", "email": "dataandgis@gmail.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "dataandgis@gmail.com was added!" in data["message"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"email": "john@gmail.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps({"username": "dataandgis", "email": "dataandgis@gmail.com"}),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps({"username": "dataandgis", "email": "dataandgis@gmail.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


# GET route
def test_single_user(test_app, test_database, add_user):
    user = add_user("Sir Ed", "sired@everest.com")
    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "Sir Ed" in data["username"]
    assert "sired@everest.com" in data["email"]


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_all_users(test_app, test_database, add_user):
    # clear the database to ensure the test runs in isolation(removes users added in previous tests).
    test_database.session.query(User).delete()
    add_user("Bert", "bert@seasamestreet.com")
    add_user("Ernie", "ernie@seasamestreet.com")
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert len(data) == 2
    assert resp.status_code == 200
    assert "Bert" in data[0]["username"]
    assert "Ernie" in data[1]["username"]
    assert "bert@seasamestreet.com" in data[0]["email"]
    assert "ernie@seasamestreet.com" in data[1]["email"]


# DELETE Route
def test_remove_user(test_app, test_database, add_user):
    test_database.session.query(User).delete() # clear database
    user = add_user("user-to-be-removed", "remove-me@seasame.com")
    client = test_app.test_client()
    resp_one = client.get("/users")
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f"/users/{user.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "remove-me@seasame.com was removed!" in data["message"]

    resp_three = client.get("/users")
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0


def test_remove_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


# sudo docker-compose exec api python -m pytest "src/tests"
# sudo docker-compose exec api python -m pytest "src/tests" --lf  (run tests that last failed)
