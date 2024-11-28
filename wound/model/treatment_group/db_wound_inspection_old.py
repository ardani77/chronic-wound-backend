from wound.model.db_setting import *
from flask import Request, Response
from bson import ObjectId
import pymongo
import json
import bson.json_util
from wound.helpers import service_h

columns = ['_id', 'wound_type_id', 'wound_area_score', 'wound_depth_score', 'wound_edge_score', 'wound_undermining_score',
           'wound_necrotic_score', 'wound_exudate_score', 'wound_surrounding_skin_score', 'wound_peripheral_edema_score',
           'wound_peripheral_induration_score', 'wound_granulation_score', 'wound_epithelialization_score']

def _get_one_wound_inspection(id: ObjectId) -> pymongo.ReturnDocument :
    filters = {'_id': id}
    return get_one_from_collection("wound_inspection", filters=filters)

def create_wound_inspection(request: Request) -> Response:
    data = {
        # '_id': ObjectId(),
        'wound_type_id': (int(request.form['wound_type_id']) if request.form['wound_type_id'] is not None else 0) if 'wound_type_id' in request.form else 0,
        'wound_area_score': (int(request.form['wound_area_score']) if request.form['wound_area_score'] is not None else 0) if 'wound_area_score' in request.form else 0,
        'wound_depth_score': (int(request.form['wound_depth_score']) if request.form['wound_depth_score'] is not None else 0) if 'wound_depth_score' in request.form else 0,
        'wound_edge_score': (int(request.form['wound_edge_score']) if request.form['wound_edge_score'] is not None else 0) if 'wound_edge_score' in request.form else 0,
        'wound_undermining_score': (int(request.form['wound_undermining_score']) if request.form['wound_undermining_score'] is not None else 0) if 'wound_undermining_score' in request.form else 0,
        'wound_necrotic_score': (int(request.form['wound_necrotic_score']) if request.form['wound_necrotic_score'] is not None else 0) if 'wound_necrotic_score' in request.form else 0,
        'wound_exudate_score': (int(request.form['wound_exudate_score']) if request.form['wound_exudate_score'] is not None else 0) if 'wound_exudate_score' in request.form else 0,
        'wound_surrounding_skin_score': (int(request.form['wound_surrounding_skin_score']) if request.form['wound_surrounding_skin_score'] is not None else 0) if 'wound_surrounding_skin_score' in request.form else 0,
        'wound_peripheral_edema_score': (int(request.form['wound_peripheral_edema_score']) if request.form['wound_peripheral_edema_score'] is not None else 0) if 'wound_peripheral_edema_score' in request.form else 0,
        'wound_peripheral_induration_score': (int(request.form['wound_peripheral_induration_score']) if request.form['wound_peripheral_induration_score'] is not None else 0) if 'wound_peripheral_induration_score' in request.form else 0,
        'wound_granulation_score': (int(request.form['wound_granulation_score']) if request.form['wound_granulation_score'] is not None else 0) if 'wound_granulation_score' in request.form else 0,
        'wound_epithelialization_score': (int(request.form['wound_epithelialization_score']) if request.form['wound_epithelialization_score'] is not None else 0) if 'wound_epithelialization_score' in request.form else 0,
    }
    new_wound_inspection_id = insert_to_collection("wound_inspection", data).inserted_id
    document_result = _get_one_wound_inspection(new_wound_inspection_id)
    return Response(response=bson.json_util.dumps(document_result), status=201, mimetype="application/json")

def get_all_wound_inspections(request: Request) -> Response:
    available_keys = columns
    unknown_query_parameter_keys = service_h.list_unknown_keys(request.args, available_keys)
    # for query in request.args:
    #     if query not in columns:
    #         return Response(response=json.dumps({'message': "Invalid query arguments"}), status=400, mimetype="application/json")
    cursor_result = get_from_collection("wound_inspection", filters=request.args)
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

def get_one_wound_inspection(request: Request, id: ObjectId) -> Response:
    document_result = _get_one_wound_inspection(id)
    if document_result is None:
        return Response(response=json.dumps({'message': "invalid Wound Inspection ID"}), status=400, mimetype="application/json")
    return Response(response=bson.json_util.dumps(dict(document_result)), status=200, mimetype="application/json")
