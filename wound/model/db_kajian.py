import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
from wound.model.db_image import *
from wound.model.db_anotasi import *
import time
import json
import bson.json_util

def get_kajian_luka(filter = {}):
    collection = get_collection("kajian_luka")
    row = collection.find(filter)
    return row

def aggregate_kajian_luka(filter):
    collection = get_collection("kajian_luka")
    row = collection.aggregate(filter)
    return row

def insert_kajian_luka(data):
    collection = get_collection("kajian_luka")
    row = collection.insert_one(data)
    return row

def update_kajian_luka(id, data):
    collection = get_collection("kajian_luka")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_kajian_luka(id):
    collection = get_collection("kajian_luka")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_kajian_baru(request):
    image_id = create_image(request)
    data ={
        "id_pasien": request.form["id_pasien"],
        "id_perawat": [request.form["id_perawat"]],
        "id_image": [image_id],
        "size": (request.form["size"]),
        "depth": (request.form["depth"]),
        "edges": (request.form["edges"]),
        "undermining": (request.form["undermining"]),
        "necrotic_amount": (request.form["necrotic_amount"]),
        "exudate_type": (request.form["exudate_type"]),
        "exudate_amount": (request.form["exudate_amount"]),
        "skinsurrounding_color": (request.form["skinsurrounding_color"]),
        "perpheral_edema": (request.form["perpheral_edema"]),
        "perpheral_induration": (request.form["perpheral_induration"]),
        "granulation": (request.form["granulation"]),
        "epithelialization": (request.form["epithelialization"]),
        "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
    }
    row = insert_kajian_luka(data)
    return "Berhasil Membuat Kajian Luka Baru"

def get_kajian_baru_by_id(id_kajian):
    data = aggregate_kajian_luka(
    [
    {
        '$match': {
            '_id': ObjectId(id_kajian)
        }
    }, 
    {
        '$lookup': {
            'from': 'image', 
            'localField': 'id_image', 
            'foreignField': '_id', 
            'as': 'image'
        }
    }
    ]
    )
    data = json.loads(bson.json_util.dumps(list(data)))
    for i in range(len(data)):
        for j in range(len(data[i]["image"])):
            anotasi = data[i]["image"][j]["id_anotasi"]['$oid']
            anotasi = get_anotasi({"_id" : ObjectId(anotasi)})
            anotasi = json.loads(bson.json_util.dumps(anotasi))[0]
            data[i]["image"][j]["anotasi"] = anotasi
    return data

def get_kajian_baru_by_id_pasien(id_pasien):
    data = aggregate_kajian_luka(
    [
    {
        '$match': {
            'id_pasien': id_pasien
        }
    }, 
    {
        '$lookup': {
            'from': 'image', 
            'localField': 'id_image', 
            'foreignField': '_id', 
            'as': 'image'
        }
    }
    ]
    )
    data = json.loads(bson.json_util.dumps(list(data)))
    for i in range(len(data)):
        for j in range(len(data[i]["image"])):
            anotasi = data[i]["image"][j]["id_anotasi"]['$oid']
            anotasi = get_anotasi({"_id" : ObjectId(anotasi)})
            anotasi = json.loads(bson.json_util.dumps(anotasi))[0]
            data[i]["image"][j]["anotasi"] = anotasi
    return data