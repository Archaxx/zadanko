from flask import Blueprint, current_app, jsonify, request

from utils.token_required import token_required

task = Blueprint('task', __name__)


@task.route("/task", methods=["POST"])
@token_required
def create_task(logged_user):
    db = current_app.config["TASK_DATABASE_SERVICE"]
    try:
        db.create_task(dict(request.form))
    except ValueError:
        return "Bad Request", 400
    return "Created", 201


@task.route("/task/<id_>", methods=["GET"])
@token_required
def get_task_by_id(logged_user, id_):
    db = current_app.config["TASK_DATABASE_SERVICE"]
    return jsonify(db.get_task_by_id(id_)), 200


@task.route("/task/<id_>", methods=["DELETE"])
@token_required
def delete_task_by_id(logged_user, id_):
    db = current_app.config["TASK_DATABASE_SERVICE"]
    db.delete_task(id_)
    return "Deleted", 200


@task.route("/task/<id_>", methods=["PUT"])
@token_required
def update_task_by_id(logged_user, id_):
    db = current_app.config["TASK_DATABASE_SERVICE"]
    db.update_task(id_, dict(request.form))
    return "Updated", 201

