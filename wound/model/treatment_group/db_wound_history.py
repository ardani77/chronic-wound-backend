from wound.model.db_setting import *
from flask import Request, Response
from bson import ObjectId
import datetime
import pymongo
import json
from wound.model.treatment_group import db_treatment
from wound.model import db_healthcare_staff_info
import bson.json_util
from wound.helpers import service_h

columns = ['_id', 'treatment_id', 'date', 'healthcare_staff_id', 'wound_inspection_id']

def get_one_wound_history_dict(id: ObjectId) -> dict:
    filters = {'_id': id}
    return dict(get_one_from_collection("wound_history", filters=filters))

def create_wound_history(request: Request) -> Response:
    ids_not_found = []
    invalid_columns = []
    id_keys = ['treatment_id', 'healthcare_staff_id', 'wound_inspection_id']
    form_request_IDs = service_h.change_request_IDs_to_ObjectId(request.form, id_keys)
    treatment_document = db_treatment.get_one_treatment(request, id=form_request_IDs['treatment_id'])
    if treatment_document is None:
        # return Response(response=json.dumps({'message': "Invalid Treatment ID"}), status=400 , mimetype="application/json")
        ids_not_found.append('treatment_id')
    date: datetime.date = None
    try:
        date = str(datetime.datetime.strptime(request.form['date'], "%Y-%m-%d").date())
    except:
        # return Response(response=json.dumps({'message': "Invalid Date"}), status=400 , mimetype="application/json")
        invalid_columns.append('date')
    healthcare_staff_document = db_healthcare_staff_info.get_one_healthcare_staff_info({"user_id": ObjectId(request.form['healthcare_staff_id'])})
    if healthcare_staff_document is None:
        # return Response(response=json.dumps({'message' : "Invalid Healthcare Staff Info ID"}), status=400, mimetype="application/json")
        ids_not_found.append('healthcare_staff_id')
    if len(ids_not_found) > 0 or len(invalid_columns) > 0:
        return Response(response=json.dumps({
            'message': "Please check invalid form inputs",
            'IDs_not_found': ids_not_found,
            'invalid_columns': invalid_columns
        }), status=400 , mimetype="application/json")
    data = {
        'date': date
    # } | form_request_IDs # Python 3.9+: Merge Operator
    }
    data.update(form_request_IDs)
    # data = {
    #     'treatment_id': ObjectId(request.form['treatment_id']),
    #     'date': date,
    #     'healthcare_staff_id': ObjectId(request.form['healthcare_staff_id']),
    #     'wound_inspection_id': ObjectId(request.form['wound_inspection_id'])
    # }
    new_wound_history_id = insert_to_collection("wound_history", data).inserted_id
    result_dict = get_one_wound_history_dict(new_wound_history_id)
    return Response(response=bson.json_util.dumps(result_dict), status=201, mimetype="application/json")

def get_all_wound_histories(request: Request) -> Response:
    available_keys = columns
    unknown_query_parameter_keys = service_h.list_unknown_keys(request.args, available_keys)
    cursor_result = get_from_collection("wound_history", filters=request.args)
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

def get_one_wound_history(request: Request, id: ObjectId) -> Response:
    result_dict = get_one_wound_history_dict(id)
    if result_dict is None:
        return Response(response=json.dumps({'message': "Invalid Wound History ID"}), status=400 , mimetype="application/json")
    return Response(response=bson.json_util.dumps(result_dict), status=200, mimetype="application/json")
