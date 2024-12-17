import json
import time
import bson
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
               "id_treatment": ObjectId(request.form["id_treatment"]),
               "id_perawat": ObjectId(request.form["id_perawat"]),
               "id_wound_inspection": ObjectId(request.form["id_wound_inspection"]),
               "created_at": time.strftime("%d/%m/%Y %H:%M:%S")
           }
    insert_to_collection("histori_kajian", data)
    return "Berhasil input histori kajian baru"

def get_histori_kajian_by_id(id_histori_kajian):
    filter = [
        {
            '$match': {
                '_id': ObjectId(id_histori_kajian)
            }
        }, {
            '$lookup': {
                'from': 'wound_inspection', 
                'localField': 'id_wound_inspection', 
                'foreignField': '_id', 
                'as': 'wound_inspection'
            }
        }
    ]
    # print(filter)
    data = aggregate_to_collection("histori_kajian", filter)
    # print("data1:", data)
    # print("testing")
    data = json.loads(bson.json_util.dumps(list(data)))
    # print("data2:", data)
    data = data[0]
    # print("data3:", data)
    if len(data)==0:
        raise Exception("Histori kajian tidak ditemukan")
    return data