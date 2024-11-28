from flask import Blueprint, request, Response
from wound.model.treatment_group import db_diabetes_tests
import json, bson
from wound.helpers import service_h

bp = Blueprint('diabetes-tests-controller', __name__)

@bp.route("/diabetes_tests", methods=["GET"])
def find_all_diabetes_tests() -> Response:
    try:
        return db_diabetes_tests.get_all_diabetes_tests(request)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/diabetes_tests/<id>", methods=["GET"])
def find_one_diabetes_tests(id: str) -> Response:
    if not bson.ObjectId.is_valid(id):
        return Response(response=json.dumps({'message' : "Invalid Medical Checkup ID"}), status=400, mimetype="application/json")
    id = bson.ObjectId(id)
    try:
        return db_diabetes_tests.get_one_diabetes_tests(request, id)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")