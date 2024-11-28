from wound.model.db_setting import *
from flask import Request, Response
from bson import ObjectId
import json, bson
from wound.model import db_patient_info
import bson.json_util
from wound.helpers import service_h

columns = ['_id', 'clinic_id', 'patient_id', 'description']
header_id_keys = ['Id', 'Clinic-Id', 'Patient-Id']
body_id_keys = ['_id', 'clinic_id', 'patient_id']
body_non_id_keys = ['description']

def get_one_treatment_dict(id: ObjectId) -> dict: # return: dict | None
    filters = {'_id': id}
    result_document = get_one_from_collection("treatment", filters=filters)
    if result_document is None:
        return None
    return dict(result_document)

def create_treatment(request: Request) -> Response:
    ids_not_found = []
    invalid_columns = []
    request_form_IDs = service_h.change_request_IDs_to_ObjectId(request.form, body_id_keys)
    # TODO: Add Clinic ID checking, currently hasn't been implemented yet
    patient_document = db_patient_info.get_one_patient_info({"user_id": request_form_IDs['patient_id']})
    if patient_document is None:
        ids_not_found.append('patient_id')
    if len(ids_not_found) > 0 or len(invalid_columns) > 0:
        return Response(response=json.dumps({
            'message': "Please check invalid form inputs",
            'IDs_not_found': ids_not_found,
            'invalid_columns': invalid_columns
        }), status=400 if len(invalid_columns) > 0 else 404, mimetype="application/json")
    data = {
        # TODO: Change line below, currently Clinic is not implemented yet
        # 'clinic_id': ObjectId(request.form['clinic_id']),
        'clinic_id': (int(request.form['clinic_id']) if request.form['clinic_id'].isdigit() else 1) if 'clinic_id' in request.form else 1,
        'patient_id': ObjectId(request.form['patient_id']),
        'description': request.form['description']
    }
    new_treatment_id = insert_to_collection("treatment", data).inserted_id
    document_result = get_one_treatment_dict(new_treatment_id)
    return Response(response=bson.json_util.dumps(document_result), status=201, mimetype="application/json")

def create_treatment(request: Request, id: ObjectId) -> dict:
    ids_not_found = []
    invalid_columns = []
    request_header_IDs = service_h.change_request_IDs_to_ObjectId(dict(request.headers), header_id_keys)
    patient_document = db_patient_info.get_one_patient_info({"user_id": request_header_IDs['Patient-Id']})
    if patient_document is None:
        ids_not_found.append('patient_id')
    if len(ids_not_found) > 0 or len(invalid_columns) > 0:
        return Response(response=json.dumps({
            'message': "Please check invalid form inputs",
            'IDs_not_found': ids_not_found,
            'invalid_columns': invalid_columns
        }), status=400 if len(invalid_columns) > 0 else 404, mimetype="application/json")
    data = {
        '_id': id,
        'clinic_id': (int(request.headers['Clinic-Id']) if request.headers['Clinic-Id'].isdigit() else 1) if 'Clinic-Id' in request.headers else 1,
        'patient_id': request_header_IDs['Patient-Id'],
        'description': request.form['description'] if 'description' in request.form else None
    }
    new_treatment_id = insert_to_collection("treatment", data).inserted_id
    result = get_one_treatment_dict(new_treatment_id)
    return result

def get_all_treatments(request: Request) -> Response:
# def get_all_treatments(request: Request, additional_message: str = "", unknown_keys: list[str] = []) -> Response:
    # for query in request.args:
    #     if query not in columns:
    #         if len(additional_message) > 0:
    #             return Response(response=json.dumps({'message' : "Invalid query arguments", 'additional_message': additional_message}), status=400, mimetype="application/json")
    #         else:
    #             return Response(response=json.dumps({'message' : "Invalid query arguments"}), status=400, mimetype="application/json")
    available_keys = columns
    unknown_query_parameter_keys = service_h.list_unknown_keys(request.args, available_keys)
    cursor_result = get_from_collection("treatment", filters=request.args)
    document_list = []
    for bson_document in cursor_result:
        document_list.append(dict(bson_document))
    if len(unknown_query_parameter_keys) > 0:
        return Response(response=bson.json_util.dumps({
            'result': document_list,
            'available_query_parameter_keys': available_keys,
            'unknown_query_parameter_keys': unknown_query_parameter_keys
        }), status=200, mimetype="application/json")
    return Response(response=bson.json_util.dumps(document_list), status=200, mimetype="application/json")

def get_one_treatment(request: Request, id: ObjectId) -> Response:
    result = get_one_treatment_dict(id)
    if result is None:
        return Response(response=json.dumps({'message' : f"Treatment with ID \'{id}\' not found"}), status=404, mimetype="application/json")
    return Response(response=bson.json_util.dumps(result), status=200, mimetype="application/json")

def update_one_treatment(request: Request, id: ObjectId) -> Response:
    result = get_one_treatment_dict(id)
    if result is None:
        return Response(response=json.dumps({'message' : f"Treatment with ID \'{id}\' not found"}), status=404, mimetype="application/json")
    
    ids_not_found = []
    invalid_columns = []
    request_header_IDs = service_h.change_request_IDs_to_ObjectId(dict(request.headers), header_id_keys)
    if 'Patient-Id' in request.headers:
        patient_document = db_patient_info.get_one_patient_info({"user_id": request_header_IDs['Patient-Id']})
        if patient_document is None:
            ids_not_found.append('patient_id')
    if len(ids_not_found) > 0 or len(invalid_columns) > 0:
        return Response(response=json.dumps({
            'message': "Please check invalid form inputs",
            'IDs_not_found': ids_not_found,
            'invalid_columns': invalid_columns
        }), status=400 if len(invalid_columns) > 0 else 404, mimetype="application/json")
    new_data = {
        'clinic_id': (int(request.headers['Clinic-Id']) if request.headers['Clinic-Id'].isdigit() else None) if 'Clinic-Id' in request.headers else None,
        'patient_id': request_header_IDs['Patient-Id'],
        'description': request.form['description'] if 'description' in request.form else None
    }
    new_data_items = list(new_data.items())
    for key, value in new_data_items:
        if value is None:
            new_data.pop(key)
    
    update_from_collection("treatment", id, new_data)
    result = get_one_treatment_dict(id)
    return Response(response=bson.json_util.dumps(result), status=200, mimetype="application/json")

def replace_one_treatment(request: Request, id: ObjectId) -> Response:
    result = get_one_treatment_dict(id)
    if result is None:
        return Response(response=json.dumps({'message' : f"Treatment with ID \'{id}\' not found"}), status=404, mimetype="application/json")
    
    ids_not_found = []
    invalid_columns = []
    request_header_IDs = service_h.change_request_IDs_to_ObjectId(dict(request.headers), header_id_keys)
    patient_document = db_patient_info.get_one_patient_info({"user_id": request_header_IDs['Patient-Id']})
    if patient_document is None:
        ids_not_found.append('patient_id')
    if len(ids_not_found) > 0 or len(invalid_columns) > 0:
        return Response(response=json.dumps({
            'message': "Please check invalid form inputs",
            'IDs_not_found': ids_not_found,
            'invalid_columns': invalid_columns
        }), status=400 if len(invalid_columns) > 0 else 404, mimetype="application/json")
    new_data = {
        'clinic_id': (int(request.headers['Clinic-Id']) if request.headers['Clinic-Id'].isdigit() else 1) if 'Clinic-Id' in request.headers else 1,
        'patient_id': request_header_IDs['Patient-Id'],
        'description': request.form['description'] if 'description' in request.form else None
    }
    
    replace_from_collection("treatment", id, new_data)
    result = get_one_treatment_dict(id)
    return Response(response=bson.json_util.dumps(result), status=200, mimetype="application/json")

def delete_treatment(request: Request, id: ObjectId) -> Response:
    result = get_one_treatment_dict(id)
    if result is None:
        return Response(response=json.dumps({'message' : f"Treatment with ID \'{id}\' not found"}), status=404, mimetype="application/json")
    delete_from_collection("treatment", id)
    return Response(response=bson.json_util.dumps(result), status=200, mimetype="application/json")
