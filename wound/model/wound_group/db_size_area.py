import json
import bson
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *

def get_size_area(filter = {}):
    collection = get_collection("size_area")
    row = collection.find(filter)
    return row

def insert_size_area(data):
    collection = get_collection("size_area")
    row = collection.insert_one(data)
    return row

def update_size_area(id, data):
    collection = get_collection("size_area")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_size_area(id):
    collection = get_collection("size_area")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_size_area(request):
    data = {
               "nomor": request.form["nomor"],
               "deskripsi": request.form["deskripsi"]
           }
    row = insert_size_area(data)
    return "Berhasil input wound area baru"

def get_size_area_by_id(id_size_area):
    filter = [
        {
            '$match': {
                '_id': ObjectId(id_size_area)
            }
        }, {
            '$lookup': {
                'from': 'size_area', 
                'localField': 'id_size_area', 
                'foreignField': '_id', 
                'as': 'size_area'
            }
        }
    ]
    data = aggregate_to_collection("size_area", filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    data = data[0]
    if len(data)==0:
        raise Exception("Size area tidak ditemukan")
    return data

def get_all_size_area():
    data = get_size_area()
    print("data1:", data)
    data = json.loads(bson.json_util.dumps(list(data)))
    print("data2:", data)
    if len(data)==0:
        raise Exception("Size area tidak ditemukan")
    return data