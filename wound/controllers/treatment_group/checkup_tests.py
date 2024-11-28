from flask import Blueprint, request, Response
from wound.model.treatment_group import db_checkup_tests
import json, bson
from wound.helpers import service_h

bp = Blueprint('checkup-tests-controller', __name__)

@bp.route("/checkup_tests", methods=["GET"])
def find_all_checkup_tests() -> Response:
    try:
        return db_checkup_tests.get_all_checkup_tests(request)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/checkup_tests/<id>", methods=["GET"])
def find_one_checkup_tests(id: str) -> Response:
    if not bson.ObjectId.is_valid(id):
        return Response(response=json.dumps({'message' : "Invalid Medical Checkup ID"}), status=400, mimetype="application/json")
    id = bson.ObjectId(id)
    try:
        return db_checkup_tests.get_one_checkup_tests(request, id)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")