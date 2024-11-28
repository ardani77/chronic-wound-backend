from flask import Blueprint, request, Response
from wound.model.treatment_group import db_checkup_test
import json, bson
from wound.helpers import service_h

bp = Blueprint('checkup-test-controller', __name__)

@bp.route("/checkup_test", methods = ["POST"])
def create_checkup_test():
    try:
       return db_checkup_test.create_checkup_test(request)
    except Exception as ex:
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")
    
@bp.route("/checkup_test/<patient_id>", methods = ["GET"])
def get_checkup_test_by_patient_id(patient_id):
    try:
       return db_checkup_test.get_checkup_test_by_patient_id(patient_id)
    except Exception as ex:
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")