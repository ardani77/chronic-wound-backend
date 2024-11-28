from wound.model.db_setting import *
from flask import Request, Response
from bson import ObjectId, Decimal128
import json
import bson.json_util
from wound.helpers import service_h, string_h
from decimal import Decimal

columns = ['_id', 'A1C', 'fasting_blood_sugar', 'glucose_tolerance', 'random_blood_sugar']
id_keys = ['Id']

def get_one_diabetes_tests_dict(id: ObjectId) -> dict: # return: dict | None
    filters = {'_id': id}
    result = get_one_from_collection("diabetes_tests", filters=filters)
    if result is None:
        return result
    result = dict(result)
    return result

def create_diabetes_tests(request: Request, id: ObjectId) -> dict:
    data = {
        '_id': id,
        'A1C': (Decimal128(round(Decimal(request.form['A1C']), 2)) if string_h.is_decimal(request.form['A1C']) else None) if 'A1C' in request.form else None,
        'fasting_blood_sugar': request.form['fasting_blood_sugar'] if 'fasting_blood_sugar' in request.form else None,
        'glucose_tolerance': request.form['glucose_tolerance'] if 'glucose_tolerance' in request.form else None,
        'random_blood_sugar': request.form['random_blood_sugar'] if 'random_blood_sugar' in request.form else None
    }
    new_diabetes_tests_id = insert_to_collection("diabetes_tests", data).inserted_id # New inserted ID should be the same as passed ID
    return get_one_diabetes_tests_dict(new_diabetes_tests_id)

def get_all_diabetes_tests(request: Request) -> Response:
    available_keys = columns
    unknown_query_parameter_keys = service_h.list_unknown_keys(request.args, available_keys)
    cursor_result = get_from_collection("diabetes_tests", filters=request.args)
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

def get_one_diabetes_tests(request: Request, id: ObjectId) -> Response:
    result_dict = get_one_diabetes_tests_dict(id)
    if result_dict is None:
        return Response(response=json.dumps({'message': f"Diabetes Tests with ID \'{id}\' not found"}), status=404 , mimetype="application/json")
    return Response(response=bson.json_util.dumps(result_dict), status=200, mimetype="application/json")

def update_one_diabetes_tests(request: Request, id: ObjectId) -> dict:
    result_dict = get_one_diabetes_tests_dict(id)
    if result_dict is None:
        return Response(response=json.dumps({'message': f"Diabetes Tests with ID \'{id}\' not found"}), status=404 , mimetype="application/json")
    new_data = {
        'A1C': (Decimal128(round(Decimal(request.form['A1C']), 2)) if string_h.is_decimal(request.form['A1C']) else None) if 'A1C' in request.form else None,
        'fasting_blood_sugar': request.form['fasting_blood_sugar'] if 'fasting_blood_sugar' in request.form else None,
        'glucose_tolerance': request.form['glucose_tolerance'] if 'glucose_tolerance' in request.form else None,
        'random_blood_sugar': request.form['random_blood_sugar'] if 'random_blood_sugar' in request.form else None
    }
    new_data_items = list(new_data.items())
    for key, value in new_data_items:
        if value is None:
            new_data.pop(key)
    # result_dict.update(new_data)
    update_from_collection("diabetes_tests", id, new_data)
    return result_dict

def replace_one_diabetes_tests(request: Request, id: ObjectId) -> dict:
    result_dict = get_one_diabetes_tests_dict(id)
    if result_dict is None:
        return Response(response=json.dumps({'message': f"Diabetes Tests with ID \'{id}\' not found"}), status=404 , mimetype="application/json")
    new_data = {
        'A1C': (Decimal128(round(Decimal(request.form['A1C']), 2)) if string_h.is_decimal(request.form['A1C']) else None) if 'A1C' in request.form else None,
        'fasting_blood_sugar': request.form['fasting_blood_sugar'] if 'fasting_blood_sugar' in request.form else None,
        'glucose_tolerance': request.form['glucose_tolerance'] if 'glucose_tolerance' in request.form else None,
        'random_blood_sugar': request.form['random_blood_sugar'] if 'random_blood_sugar' in request.form else None
    }
    # result_dict.update(new_data)
    replace_from_collection("diabetes_tests", id, new_data)
    return result_dict
