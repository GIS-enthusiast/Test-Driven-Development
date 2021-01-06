# src/api/ping.py


# from flask import Blueprint
from flask_restx import Namespace, Resource  # ,Api

ping_namespace = Namespace("ping")

# replacing blueprints with Namespace
# ping_blueprint = Blueprint("ping", __name__)
# api = Api(ping_blueprint)


class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "pong"}


# api.add_resource(Ping, "/ping")
ping_namespace.add_resource(Ping, "")
