from datetime import datetime, timedelta

import jwt
from flask import Blueprint, current_app, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from services.task_database_service import Status
from utils.token_required import token_required

user = Blueprint('user', __name__)


@user.route("/user/<user_id>/tasks", methods=["GET"])
@token_required
def get_task_for_user(logged_user, user_id):
    db = current_app.config["TASK_DATABASE_SERVICE"]
    return jsonify(db.get_task_for_user(user_id)), 200


@user.route("/user/<user_id>/tasks/not_done", methods=["GET"])
@token_required
def get_not_done_task_for_user(logged_user, user_id):
    db = current_app.config["TASK_DATABASE_SERVICE"]
    return jsonify(db.get_task_for_user(user_id, status=Status.NOT_DONE.value)), 200


@user.route("/register", methods=["POST"])
def register():
    db = current_app.config["USER_DATABASE_SERVICE"]
    data = request.get_json()
    hashed_password = generate_password_hash(data.get("password"), method="sha256")
    data["password"] = hashed_password
    try:
        db.create_user(data)
    except ValueError:
        return "Conflict", 409
    return "Created", 201


@user.route("/login", methods=["POST"])
def login():
    db = current_app.config["USER_DATABASE_SERVICE"]
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return "could not verify", 401

    login_user = db.get_user_by_name(auth.username)

    if check_password_hash(login_user.password, auth.password):
        token = jwt.encode({
            "public_id": login_user.id,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        },
            current_app.config["SECRET_KEY"])
        return jsonify(token)

    return "could not verify", 401
