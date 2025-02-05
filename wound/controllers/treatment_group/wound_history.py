from flask import Blueprint, request, Response
from wound.model.treatment_group import db_wound_history
import json, bson
from wound.helpers import service_h

bp = Blueprint('wound-history-controller', __name__)

# @bp.route("/wound_history", methods=["POST"])
# def create_wound_history() -> Response:
#     required_keys = ['treatment_id', 'date', 'healthcare_staff_id', 'wound_inspection_id']
#     missing_keys = service_h.list_missing_keys(request.form, required_keys)
#     missing_keys_count = len(missing_keys)
#     available_keys = db_wound_history.columns[1:]
#     unknown_keys = service_h.list_unknown_keys(request.form, available_keys)
#     unknown_keys_count = len(unknown_keys)
#     id_keys = ['treatment_id', 'healthcare_staff_id', 'wound_inspection_id']
#     invalid_ObjectId_list = service_h.valid_ObjectId_checks(request.form, id_keys)
#     invalid_id_count = len(invalid_ObjectId_list)
#     if missing_keys_count > 0 or unknown_keys_count > 0 or invalid_id_count > 0:
#         return Response(response=json.dumps({
#             'message' : "Please check form inputs",
#             'required_keys': required_keys,
#             'missing_keys': missing_keys,
#             'missing_keys_count': missing_keys_count,
#             'invalid_IDs': invalid_ObjectId_list,
#             'invalid_ID_count': invalid_id_count,
#             'available_keys': available_keys,
#             'unknown_keys': unknown_keys,
#             'unknown_keys_count': unknown_keys_count
#             }), status=400, mimetype="application/json")
#     try:
#        return db_wound_history.create_wound_history(request)
#     except Exception as ex:
#         print(ex)
#         return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

# @bp.route("/wound_history", methods=["GET"])
# def find_all_wound_histories() -> Response:
#     try:
#        return db_wound_history.get_all_wound_histories(request)
#     except Exception as ex:
#         print(ex)
#         return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

# @bp.route("/wound_history/<id>", methods=["GET"])
# def find_one_wound_history(id: str) -> Response:
#     if not bson.ObjectId.is_valid(id):
#         return Response(response=json.dumps({'message' : "Invalid Wound History ID"}), status=400, mimetype="application/json")
#     id = bson.ObjectId(id)
#     try:
#        return db_wound_history.get_one_wound_history(request, id)
#     except Exception as ex:
#         print(ex)
#         return Response(response=json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")