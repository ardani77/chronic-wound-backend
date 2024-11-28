from wound.model.db_setting import *
from flask import Request, Response
from bson import ObjectId, Decimal128
import json
import bson.json_util
from wound.helpers import service_h, string_h
from decimal import Decimal
from wound.model.treatment_group import db_diabetes_tests

columns = ['_id', 'blood_pressure', 'heart_rate', 'pulse_rate', 'tension_level_id', 'body_temperature', 'body_temperature_unit_id', 'abpi', 'medical_history']
id_keys = ['id']

def get_one_checkup_tests_dict(id: ObjectId) -> dict: # return: dict | None
    diabetes_tests_dict = db_diabetes_tests.get_one_diabetes_tests_dict(id)
    diabetes_tests_dict.pop('_id')
    filters = {'_id': id}
    checkup_tests_document = get_one_from_collection("checkup_tests", filters=filters)
    if checkup_tests_document is None:
        return None
    checkup_tests_dict = dict(checkup_tests_document)
    checkup_tests_dict.update({
        'diabetes_tests': diabetes_tests_dict
    })
    return checkup_tests_dict

def create_checkup_tests(request: Request, id: ObjectId) -> dict:
    data = {
        '_id': id,
        'blood_pressure': request.form['blood_pressure'] if 'blood_pressure' in request.form else None,
        'heart_rate': request.form['heart_rate'] if 'heart_rate' in request.form else (request.form['pulse_rate'] if 'pulse_rate' in request.form else None),
        'pulse_rate': request.form['pulse_rate'] if 'pulse_rate' in request.form else (request.form['heart_rate'] if 'heart_rate' in request.form else None),
        'tension_level_id': (int(request.form['tension_level_id']) if request.form['tension_level_id'].isdigit() else 0) if 'tension_level_id' in request.form else 0,
        'body_temperature': (Decimal128(round(Decimal(request.form['body_temperature']), 2)) if string_h.is_decimal(request.form['body_temperature']) else None) if 'body_temperature' in request.form else None,
        'body_temperature_unit_id': (int(request.form['body_temperature_unit_id']) if request.form['body_temperature_unit_id'].isdigit() else 0) if 'body_temperature_unit_id' in request.form else 0,
        'abpi': (Decimal128(round(Decimal(request.form['abpi']), 2)) if string_h.is_decimal(request.form['abpi']) else None) if 'abpi' in request.form else None,
        'medical_history': request.form['medical_history'] if 'medical_history' in request.form else None
    }
    # No need, because they have the same ID
    # new_checkup_tests_id = insert_to_collection("checkup_tests", data).inserted_id
    insert_to_collection("checkup_tests", data)
    
    # diabetes_tests_dict = dict(db_diabetes_tests._create_diabetes_tests(request, new_checkup_tests_id))
    # db_diabetes_tests._create_diabetes_tests(request, new_checkup_tests_id)
    # checkup_tests_dict = get_one_checkup_tests_dict(new_checkup_tests_id)
    # checkup_tests_dict.update({
    #     'diabetes_tests': diabetes_tests_dict
    # })
    db_diabetes_tests.create_diabetes_tests(request, id)
    checkup_tests_dict = get_one_checkup_tests_dict(id)
    return checkup_tests_dict
    # return Response(response=bson.json_util.dumps(result_dict), status=201, mimetype="application/json")

def get_all_checkup_tests(request: Request) -> Response:
    available_keys = columns
    unknown_query_parameter_keys = service_h.list_unknown_keys(request.args, available_keys)
    cursor_result = get_from_collection("checkup_tests", filters=request.args)
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

def get_one_checkup_tests(request: Request, id: ObjectId) -> Response:
    result_dict = get_one_checkup_tests_dict(id)
    if result_dict is None:
        return Response(response=json.dumps({'message': f"Checkup Tests with ID \'{id}\' not found"}), status=404 , mimetype="application/json")
    return Response(response=bson.json_util.dumps(result_dict), status=200, mimetype="application/json")

def update_one_checkup_tests(request: Request, id: ObjectId) -> dict:
    checkup_tests_dict = get_one_checkup_tests_dict(id)
    if checkup_tests_dict is None:
        return Response(response=json.dumps({'message': f"Checkup Tests with ID \'{id}\' not found"}), status=404 , mimetype="application/json")
    new_data = {
        'blood_pressure': request.form['blood_pressure'] if 'blood_pressure' in request.form else None,
        'pulse': request.form['pulse'] if 'pulse' in request.form else None,
        'tension_level_id': (int(request.form['tension_level_id']) if request.form['tension_level_id'].isdigit() else None) if 'tension_level_id' in request.form else None,
        'body_temperature': (Decimal128(round(Decimal(request.form['body_temperature']), 2)) if string_h.is_decimal(request.form['body_temperature']) else None) if 'body_temperature' in request.form else None,
        'body_temperature_unit': (int(request.form['body_temperature_unit']) if request.form['body_temperature_unit'].isdigit() else None) if 'body_temperature_unit' in request.form else None,
        'abpi': (Decimal128(round(Decimal(request.form['abpi']), 2)) if string_h.is_decimal(request.form['abpi']) else None) if 'abpi' in request.form else None,
        'medical_history': request.form['medical_history'] if 'medical_history' in request.form else None
    }
    new_data_items = list(new_data.items())
    for key, value in new_data_items:
        if value is None:
            new_data.pop(key)
    # checkup_tests_dict.update(new_data)
    
    db_diabetes_tests.update_one_diabetes_tests(request, id)
    update_from_collection("checkup_tests", id, new_data)
    result_dict = get_one_checkup_tests_dict(id)
    
    return result_dict

def replace_one_checkup_tests(request: Request, id: ObjectId) -> dict:
    result_dict = get_one_checkup_tests_dict(id)
    if result_dict is None:
        return Response(response=json.dumps({'message': f"Checkup Tests with ID \'{id}\' not found"}), status=404 , mimetype="application/json")
    new_data = {
        'blood_pressure': request.form['blood_pressure'] if 'blood_pressure' in request.form else None,
        'pulse': request.form['pulse'] if 'pulse' in request.form else None,
        'tension_level_id': (int(request.form['tension_level_id']) if request.form['tension_level_id'].isdigit() else 0) if 'tension_level_id' in request.form else 0,
        'body_temperature': (Decimal128(round(Decimal(request.form['body_temperature']), 2)) if string_h.is_decimal(request.form['body_temperature']) else None) if 'body_temperature' in request.form else None,
        'body_temperature_unit': (int(request.form['body_temperature_unit']) if request.form['body_temperature_unit'].isdigit() else 0) if 'body_temperature_unit' in request.form else 0,
        'abpi': (Decimal128(round(Decimal(request.form['abpi']), 2)) if string_h.is_decimal(request.form['abpi']) else None) if 'abpi' in request.form else None,
        'medical_history': request.form['medical_history'] if 'medical_history' in request.form else None
    }
    # result_dict.update(new_data)
    
    db_diabetes_tests.update_one_diabetes_tests(request, id)
    replace_from_collection("checkup_tests", id, new_data)
    result_dict = get_one_checkup_tests_dict(id)
    
    return result_dict
