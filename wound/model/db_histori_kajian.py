import time
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *

def get_histori_kajian(filter = {}):
    collection = get_collection("histori_kajian")
    row = collection.find(filter)
    return row

def insert_histori_kajian(data):
    collection = get_collection("histori_kajian")
    row = collection.insert_one(data)
    return row

def update_histori_kajian(id, data):
    collection = get_collection("histori_kajian")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_histori_kajian(id):
    collection = get_collection("histori_kajian")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_histori_kajian(request):
    data = {
               "id_treatment": int(request.form["id_treatment"]),
               "id_perawat": int(request.form["id_perawat"]),
               "id_wound_inspection": int(request.form["id_wound_inspection"]),
               "created_at": time.strftime("%d/%m/%Y %H:%M:%S")
            #    "created_at": '${currentDate}'
        #        currentDate: {
        # "created_at": { '$type': "timestamp" }
        #    }
           }
    insert_to_collection("histori_kajian", data)
    return "Berhasil input histori kajian baru"

def get_histori_kajian_by_id(histori_kajian_id):
    filter = [
    {
        '$match': {
            '_id': ObjectId(histori_kajian_id)
        }
    }, {
        # '$lookup': {
        #     'from': 'image', 
        #     'localField': 'image_id', 
        #     'foreignField': '_id', 
        #     'pipeline': [
        #         {
        #             '$lookup': {
        #                 'from': 'wound_annotation', 
        #                 'localField': 'wound_annotation_id', 
        #                 'foreignField': '_id', 
        #                 'as': 'wound_annotation'
        #             }
        #         }
        #     ], 
        #     'as': 'image'
        # }
    }]
    data = aggregate_to_collection("histori_kajian",filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    if len(data)==0:
        raise Exception("Histori kajian tidak ditemukan")
    return data