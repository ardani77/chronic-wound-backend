from flask import Blueprint, request, Response
from wound.model.treatment_group import db_wound_inspection
import json, bson
from wound.helpers import service_h

bp = Blueprint('wound-inspection-controller', __name__)

@bp.route("/wound_inspection", methods = ["POST"])
def create_wound_inspection():
    try:
       return json.dumps({"message" : str(db_wound_inspection.create_wound_inspection(request)) })
    except Exception as ex:
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")
    
@bp.route("/wound_inspection/patient/<patient_id>",methods=["GET"])
def get_wound_inspection_by_patient_id(patient_id):
    try:
       return db_wound_inspection.get_wound_inspection_by_patient_id(patient_id)
    except Exception as ex:
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")
    
@bp.route("/wound_inspection/<wound_inspection_id>",methods = ["GET"])
def get_wound_inspection_by_id(wound_inspection_id):
    try:
       return db_wound_inspection.get_wound_inspection_by_id(wound_inspection_id)
    except Exception as ex:
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")