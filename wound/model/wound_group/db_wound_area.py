import json
import bson
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *

def get_wound_area(filter = {}):
    collection = get_collection("wound_area")
    row = collection.find(filter)
    return row

def insert_wound_area(data):
    collection = get_collection("wound_area")
    row = collection.insert_one(data)
    return row

def update_wound_area(id, data):
    collection = get_collection("wound_area")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_wound_area(id):
    collection = get_collection("wound_area")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_wound_area(request):
    data = {
               "nomor": request.form["nomor"],
               "deskripsi": request.form["deskripsi"]
           }
    row = insert_wound_area(data)
    return "Berhasil input wound area baru"

def get_wound_area_by_id(id_wound_area):
    filter = [
        {
            '$match': {
                '_id': ObjectId(id_wound_area)
            }
        }, {
            '$lookup': {
                'from': 'wound_area', 
                'localField': 'id_wound_area', 
                'foreignField': '_id', 
                'as': 'wound_area'
            }
        }
    ]
    data = aggregate_to_collection("wound_area", filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    data = data[0]
    if len(data)==0:
        raise Exception("Wound Area tidak ditemukan")
    return data

def get_all_wound_area():
    data = get_wound_area()
    data = json.loads(bson.json_util.dumps(list(data)))
    if len(data)==0:
        raise Exception("Wound area tidak ditemukan")
    return data