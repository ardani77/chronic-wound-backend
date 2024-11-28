from flask import Blueprint, request, Response
from wound.model.treatment_group import db_medical_checkup, db_checkup_tests, db_diabetes_tests, db_treatment
import json, bson
from wound.helpers import service_h

bp = Blueprint('medical-checkup-controller', __name__)

available_keys = db_medical_checkup.columns[1:] + db_checkup_tests.columns[1:] + db_diabetes_tests.columns[1:] + db_treatment.columns[1:] # Similar to list.extend()
required_header_keys = ['Patient-Id', 'Healthcare-Staff-Id']
required_body_keys = []
id_keys = db_medical_checkup.id_keys[1:] + db_checkup_tests.id_keys[1:] + db_diabetes_tests.id_keys[1:] + db_treatment.header_id_keys[1:]

@bp.route("/medical_checkup", methods=["POST"])
def create_medical_checkup() -> Response:
    # required_body_keys = ['treatment_id']
    missing_header_keys = service_h.list_missing_keys(dict(request.headers), required_header_keys)
    # print(dict(request.headers))
    missing_header_keys_count = len(missing_header_keys)
    missing_body_keys = service_h.list_missing_keys(request.form, required_body_keys)
    missing_body_keys_count = len(missing_body_keys)
    unknown_keys = service_h.list_unknown_keys(request.form, available_keys)
    unknown_keys_count = len(unknown_keys)
    # id_keys = ['treatment_id']
    invalid_ObjectId_list = service_h.valid_ObjectId_checks(request.headers, id_keys)
    # invalid_ObjectId_list += service_h.valid_ObjectId_checks(request.form, id_keys)
    invalid_id_count = len(invalid_ObjectId_list)
    if missing_header_keys_count > 0 or missing_body_keys_count > 0 or unknown_keys_count > 0 or invalid_id_count > 0:
        return Response(response=json.dumps({
            'message' : "Please check form inputs",
            'required_header_keys': required_header_keys,
            'missing_header_keys': missing_header_keys,
            'missing_header_keys_count': missing_header_keys_count,
            'required_body_keys': required_body_keys,
            'missing_body_keys': missing_body_keys,
            'missing_body_keys_count': missing_body_keys_count,
            'invalid_IDs': invalid_ObjectId_list,
            'invalid_ID_count': invalid_id_count,
            'available_keys': available_keys,
            'unknown_keys': unknown_keys,
            'unknown_keys_count': unknown_keys_count
            }), status=400, mimetype="application/json")
    try:
        return db_medical_checkup.create_medical_checkup(request)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/medical_checkup", methods=["GET"])
def find_all_medical_checkups() -> Response:
    try:
        return db_medical_checkup.get_all_medical_checkups(request)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/medical_checkup/<id>", methods=["GET"])
def find_one_medical_checkup(id: str) -> Response:
    if not bson.ObjectId.is_valid(id):
        return Response(response=json.dumps({'message' : "Invalid Medical Checkup ID"}), status=400, mimetype="application/json")
    id = bson.ObjectId(id)
    try:
        return db_medical_checkup.get_one_medical_checkup(request, id)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/medical_checkup/<id>", methods=["PATCH"])
def update_one_medical_checkup(id: str) -> Response:
    if not bson.ObjectId.is_valid(id):
        return Response(response=json.dumps({'message' : "Invalid Medical Checkup ID"}), status=400, mimetype="application/json")
    id = bson.ObjectId(id)
    
    unknown_keys = service_h.list_unknown_keys(request.form, available_keys)
    unknown_keys_count = len(unknown_keys)
    invalid_ObjectId_list = service_h.valid_ObjectId_checks(request.headers, id_keys)
    invalid_id_count = len(invalid_ObjectId_list)
    if unknown_keys_count > 0 or invalid_id_count > 0:
        return Response(response=json.dumps({
            'message' : "Please check form inputs",
            'invalid_IDs': invalid_ObjectId_list,
            'invalid_ID_count': invalid_id_count,
            'available_keys': available_keys,
            'unknown_keys': unknown_keys,
            'unknown_keys_count': unknown_keys_count
            }), status=400, mimetype="application/json")
    
    try:
        return db_medical_checkup.update_one_medical_checkup(request, id)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/medical_checkup/<id>", methods=["PUT"])
def replace_one_medical_checkup(id: str) -> Response:
    if not bson.ObjectId.is_valid(id):
        return Response(response=json.dumps({'message' : "Invalid Medical Checkup ID"}), status=400, mimetype="application/json")
    id = bson.ObjectId(id)
    
    unknown_keys = service_h.list_unknown_keys(request.form, available_keys)
    unknown_keys_count = len(unknown_keys)
    invalid_ObjectId_list = service_h.valid_ObjectId_checks(request.headers, id_keys)
    invalid_id_count = len(invalid_ObjectId_list)
    if unknown_keys_count > 0 or invalid_id_count > 0:
        return Response(response=json.dumps({
            'message' : "Please check form inputs",
            'invalid_IDs': invalid_ObjectId_list,
            'invalid_ID_count': invalid_id_count,
            'available_keys': available_keys,
            'unknown_keys': unknown_keys,
            'unknown_keys_count': unknown_keys_count
            }), status=400, mimetype="application/json")
    
    try:
        return db_medical_checkup.replace_one_medical_checkup(request, id)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")
