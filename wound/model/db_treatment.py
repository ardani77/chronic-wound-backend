import json
import time
import bson
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *

def get_treatment(filter = {}):
    collection = get_collection("treatment")
    row = collection.find(filter)
    return row

def insert_treatment(data):
    collection = get_collection("treatment")
    row = collection.insert_one(data)
    return row

def update_treatment(id, data):
    collection = get_collection("treatment")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_treatment(id):
    collection = get_collection("treatment")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_treatment(request):
    data = {
               "id_klinik": ObjectId(request.form["id_klinik"]),
               "id_pasien": ObjectId(request.form["id_pasien"]),
               "description": request.form["description"]
           }
    insert_to_collection("treatment", data)
    return "Berhasil input histori kajian baru"

def get_treatment_by_id(treatment_id):
    filter = [
    {
        '$match': {
            '_id': ObjectId(treatment_id)
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
    data = aggregate_to_collection("treatment",filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    if len(data)==0:
        raise Exception("Histori kajian tidak ditemukan")
    return data