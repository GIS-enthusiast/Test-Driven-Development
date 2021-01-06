# src/api/users/views.py

from flask import request  # removed Blueprint and Api, replaced with Namespace
from flask_restx import Namespace, Resource, fields  # Api removed

from src.api.users.crud import (  # isort:skip
    get_all_users,
    get_user_by_email,
    add_user,
    get_user_by_id,
    update_user,
    delete_user,
)

users_namespace = Namespace("users")

# link a Flask-RESTX API to a Flask Blueprint.
# users_blueprint = Blueprint("users", __name__)
# api = Api(users_blueprint)


# create an api model to define the shape of Userslist
user = users_namespace.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


# define the route handler.
class UsersList(Resource):
    @users_namespace.expect(user, validate=True)
    @users_namespace.response(201, "<user_email> was added!")
    @users_namespace.response(400, "Sorry. That email already exists.")
    def post(self):
        """Creates a new user."""
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_email(email)
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        add_user(username, email)

        response_object["message"] = f"{email} was added!"
        return response_object, 201

    @users_namespace.marshal_with(user, as_list=True)
    def get(self):
        """Returns all users."""
        return get_all_users(), 200


class Users(Resource):
    @users_namespace.marshal_with(
        user
    )  # user model used as a serialiser to generate a JSON object from the model's fields.
    @users_namespace.response(200, "Success")
    @users_namespace.response(404, "User <user_id> does not exist.")
    def get(self, user_id):
        """Returns a single user."""
        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        return user, 200

    @users_namespace.expect(user, validate=True)
    @users_namespace.response(200, "<user_id> was updated!")
    @users_namespace.response(400, "Sorry. That email already exists.")
    @users_namespace.response(404, "User <user_id> does not exist")
    def put(self, user_id):
        """Updates a user."""
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        if get_user_by_email(email):
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        update_user(user, username, email)

        response_object["message"] = f"{user.id} was updated!"
        return response_object, 200

    @users_namespace.response(200, "<user_id> was removed!")
    @users_namespace.response(404, "User <user_id> does not exist")
    def delete(self, user_id):
        """Deletes a user."""
        response_object = {}
        user = get_user_by_id(user_id)

        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        delete_user(user)

        response_object["message"] = f"{user.email} was removed!"
        return response_object, 200


# api.add_resource(UsersList, "/users")
# api.add_resource(Users, "/users/<int:user_id>")

users_namespace.add_resource(UsersList, "")
users_namespace.add_resource(Users, "/<int:user_id>")
