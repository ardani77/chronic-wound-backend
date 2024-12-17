# import time
# import pymongo
# from flask import current_app, g
# from flask.cli import with_appcontext
# from bson import ObjectId
# from wound.model.db_setting import *

# def get_tindakan_medis(filter = {}):
#     collection = get_collection("tindakan_medis")
#     row = collection.find(filter)
#     return row

# def insert_tindakan_medis(data):
#     collection = get_collection("tindakan_medis")
#     row = collection.insert_one(data)
#     return row

# def update_tindakan_medis(id, data):
#     collection = get_collection("tindakan_medis")
#     id=ObjectId(id)
#     filter = {"_id":id}
#     return collection.update_one(filter, data, upsert=False)

# def delete_tindakan_medis(id):
#     collection = get_collection("tindakan_medis")
#     id = ObjectId(id)
#     filter = {"_id":id}
#     return collection.delete_one(filter)

# def create_tindakan_medis(request):
#     data = {
#                "id_pasien": int(request.form["id_pasien"]),
#                "id_perawat": int(request.form["id_perawat"]),
#                "id_wound_inspection": int(request.form["id_wound_inspection"]),
#                "created_at": time.strftime("%d/%m/%Y %H:%M:%S")
#            }
#     insert_to_collection("tindakan_medis", data)
#     return "Berhasil input histori kajian baru"

# def get_tindakan_medis_by_id(tindakan_medis_id):
#     filter = [
#     {
#         '$match': {
#             '_id': ObjectId(tindakan_medis_id)
#         }
#     }, {
#         # '$lookup': {
#         #     'from': 'image', 
#         #     'localField': 'image_id', 
#         #     'foreignField': '_id', 
#         #     'pipeline': [
#         #         {
#         #             '$lookup': {
#         #                 'from': 'wound_annotation', 
#         #                 'localField': 'wound_annotation_id', 
#         #                 'foreignField': '_id', 
#         #                 'as': 'wound_annotation'
#         #             }
#         #         }
#         #     ], 
#         #     'as': 'image'
#         # }
#     }]
#     data = aggregate_to_collection("tindakan_medis",filter)
#     data = json.loads(bson.json_util.dumps(list(data)))
#     if len(data)==0:
#         raise Exception("Histori kajian tidak ditemukan")
#     return data