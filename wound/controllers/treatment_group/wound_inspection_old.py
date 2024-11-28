from flask import Blueprint, request, Response
from wound.model.treatment_group import db_wound_inspection_old
import json, bson
from wound.helpers import service_h

#bp = Blueprint('wound-inspection-controller', __name__)

@bp.route("/wound_inspection", methods=["POST"])
def create_wound_inspection() -> bson.ObjectId :
    required_keys = []
    missing_keys = service_h.list_missing_keys(request.form, required_keys)
    missing_keys_count = len(missing_keys)
    available_keys = db_wound_inspection_old.columns[1:]
    unknown_keys = service_h.list_unknown_keys(request.form, available_keys)
    unknown_keys_count = len(unknown_keys)
    if missing_keys_count > 0 or unknown_keys_count > 0:
        return Response(response=json.dumps({
            'message' : "Please check form inputs",
            'required_keys': required_keys,
            'missing_keys': missing_keys,
            'missing_keys_count': missing_keys_count,
            'available_keys': available_keys,
            'unknown_keys': unknown_keys,
            'unknown_keys_count': unknown_keys_count
            }), status=400, mimetype="application/json")
    try:
       return db_wound_inspection_old.create_wound_inspection(request)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")
    
@bp.route("/wound_inspection", methods=["GET"])
def find_all_wound_inspections():
    try:
       return db_wound_inspection_old.get_all_wound_inspections(request)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/wound_inspection/<id>", methods=["GET"])
def find_one_wound_inspection(id: str):
    if not bson.ObjectId.is_valid(id):
        return Response(response = json.dumps({'message' : "Invalid Wound Inspection ID"}), status=400, mimetype="application/json")
    id = bson.ObjectId(id)
    try:
       return db_wound_inspection_old.get_one_wound_inspection(request, id)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")