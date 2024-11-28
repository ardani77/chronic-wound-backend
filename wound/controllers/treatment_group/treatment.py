from flask import Blueprint, request, Response, Request
from wound.model.treatment_group import db_treatment
import json, bson
from wound.helpers import service_h

bp = Blueprint('treatment-controller', __name__)

available_json_keys = db_treatment.columns[1:]
available_header_keys = db_treatment.header_id_keys[1:]
available_form_keys = db_treatment.body_non_id_keys
required_json_keys = ['patient_id']
required_header_keys = ['patient_id']
required_form_keys = []
header_id_keys = db_treatment.header_id_keys[1:]
body_id_keys = db_treatment.body_id_keys[1:]

@bp.route("/treatment", methods=["POST"])
def create_treatment() -> Response:
    is_json_request = False
    if request.is_json:
        is_json_request = True
        missing_keys = service_h.list_missing_keys(request.json, required_json_keys)
    else:
        missing_keys = service_h.list_missing_keys(request.headers, required_header_keys)
        unknown_keys = service_h.list_unknown_keys(request.form, available_form_keys)
    missing_keys_count = len(missing_keys)
    unknown_keys_count = len(unknown_keys)
    # TODO: Change line below, Clinic is not implemented yet
    # id_keys = ['clinic_id', 'patient_id']
    invalid_ObjectId_list = service_h.valid_ObjectId_checks(request.json, body_id_keys)
    invalid_id_count = len(invalid_ObjectId_list)
    if missing_keys_count > 0 or unknown_keys_count > 0 or invalid_id_count > 0:
        response_body = {'message' : "Please check form inputs"}
        if is_json_request:
            response_body.update({'required_json_keys': required_json_keys})
        else:
            response_body.update({
                'required_header_keys': required_header_keys,
                'required_form_keys': required_form_keys
            })
        response_body.update({
            'missing_keys': missing_keys,
            'missing_keys_count': missing_keys_count,
            'invalid_IDs': invalid_ObjectId_list,
            'invalid_ID_count': invalid_id_count
        })
        if is_json_request:
            response_body.update({'available_json_keys': available_json_keys})
        else:
            response_body.update({
                'available_header_keys': available_header_keys,
                'available_form_keys': available_form_keys
            })
        response_body.update({
            'unknown_keys': unknown_keys,
            'unknown_keys_count': unknown_keys_count
        })
        return Response(response=json.dumps(response_body), status=400, mimetype="application/json")
    try:
        return db_treatment.create_treatment(request)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")
    
@bp.route("/treatment", methods=["GET"])
def find_all_treatments() -> Response:
    # available_keys = db_treatment.columns
    # additional_message = ""
    # unknown_keys_exist = service_h.check_unknown_keys_exist(request.args, available_keys)
    # if unknown_keys_exist:
    #     additional_message += "Unknown query key(s) exist"
    try:
        return db_treatment.get_all_treatments(request)
    #    return db_treatment.get_all_treatments(request, additional_message)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/treatment/<id>", methods=["GET"])
def find_one_treatment(id: str) -> Response:
    invalid_count = 0
    bad_request_message = ""
    if not bson.ObjectId.is_valid(id):
        invalid_count += 1
        bad_request_message += "Invalid Treatment ID, "
    if invalid_count > 0:
        bad_request_message = bad_request_message[:-2]
        return Response(response=json.dumps({'message' : bad_request_message, 'invalid_count': invalid_count}), status=400, mimetype="application/json")
    id = bson.ObjectId(id)
    try:
        return db_treatment.get_one_treatment(request, id)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/treatment/patient/<patient_id>", methods=["GET"])
def find_treatments_with_patient_id(patient_id: str) -> Response:
    invalid_count = 0
    bad_request_message = ""
    if not bson.ObjectId.is_valid(patient_id):
        invalid_count += 1
        bad_request_message += "Invalid Patient ID, "
    if invalid_count > 0:
        bad_request_message = bad_request_message[:-2]
        return Response(response=json.dumps({'message' : bad_request_message, 'invalid_count': invalid_count}), status=400, mimetype="application/json")
    patient_id = bson.ObjectId(patient_id)
    try:
        return db_treatment.get_treatments_with_patient_id(request, patient_id)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/treatment/clinic/<clinic_id>", methods=["GET"])
def find_treatments_with_clinic_id(clinic_id: str) -> Response:
    invalid_count = 0
    bad_request_message = ""
    # TODO: Currently, Clinic ID may be of integer type
    clinic_id_is_valid_ObjectId = bson.ObjectId.is_valid(clinic_id)
    clinic_id_is_valid_number = clinic_id.isdigit()
    if not clinic_id_is_valid_ObjectId and not clinic_id_is_valid_number:
        invalid_count += 1
        bad_request_message += "Invalid Clinic ID, "
    if invalid_count > 0:
        bad_request_message = bad_request_message[:-2]
        return Response(response=json.dumps({'message' : bad_request_message, 'invalid_count': invalid_count}), status=400, mimetype="application/json")
    if clinic_id_is_valid_ObjectId:
        clinic_id = bson.ObjectId(clinic_id)
    if clinic_id_is_valid_number:
        clinic_id = int(clinic_id)
    try:
        return db_treatment.get_treatments_with_clinic_id(request, clinic_id)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/treatment/<id>", methods=['PATCH'])
def update_one_treatment(id: str) -> Response:
    if id is None or len(id) == 0 or not bson.ObjectId.is_valid(id):
        Response(response=json.dumps({'message': "Invalid Treatment ID"}), status=400, mimetype="application/json")
    try:
        return db_treatment.update_one_treatment(request)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/treatment/<id>", methods=['PUT'])
def replace_one_treatment(id: str) -> Response:
    if id is None or len(id) == 0 or not bson.ObjectId.is_valid(id):
        Response(response=json.dumps({'message': "Invalid Treatment ID"}), status=400, mimetype="application/json")
    try:
        return db_treatment.replace_one_treatment(request)
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")
