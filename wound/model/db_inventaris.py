import json
import time
import bson
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *

def get_inventaris(filter = {}):
    collection = get_collection("inventaris")
    row = collection.find(filter)
    return row

def insert_inventaris(data):
    collection = get_collection("inventaris")
    row = collection.insert_one(data)
    return row

def update_inventaris(id, data):
    collection = get_collection("inventaris")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_inventaris(id):
    collection = get_collection("inventaris")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_inventaris(request):
    check  = get_from_collection("patient_info",{"user_id":ObjectId(request.form["patient_id"])})
    check = json.loads(bson.json_util.dumps(list(check)))
    if len(check) == 0:
        raise Exception("Pasien tidak ditemukan")
    # data = {
    #     "patient_id" : ObjectId(request.form["patient_id"])
    # }
    check2  = get_from_collection("healthcare_staff_info",{"user_id":ObjectId(request.form["healthcare_staff_id"])})
    check2 = json.loads(bson.json_util.dumps(list(check2)))
    if len(check2) == 0:
        raise Exception("Perawat tidak ditemukan")
    # data = {
    #     "healthcare_staff_id" : ObjectId(request.form["healthcare_staff_id"])
    # }
    data = {
        "clinic_id" : ObjectId("66bb21acfdc1be5a6ca38fb0"),
        "patient_id" : ObjectId(request.form["patient_id"]),
        "healthcare_staff_id" : ObjectId(request.form["healthcare_staff_id"]),
        "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
        "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S")
    }
    nullable = {"kain_kasa": "string",
               "kapas": "string",
               "plester": "string",
               "alkohol": "string",
               "lainnya": "string",
               "resep_obat": "string"}
    for param in nullable.keys():
        if request.form.get(param)!='""' and request.form.get(param)!="" and request.form.get(param)!="''" and request.form.get(param)!=None:
            if nullable[param]=="string":
                data[param] = request.form[param]
            elif nullable[param]=="int":
                data[param] = int(request.form[param])
            elif nullable[param]=="date":
                data[param] = request.form[param]
            elif nullable[param]=="float":
                data[param] = float(request.form[param])
        else:
            data[param] = None
    # data = {
    #     "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
    #     "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
    # }
    data = insert_inventaris(data)
    return data.inserted_id

def get_inventaris_by_id(id_inventaris):
    filter = [
        {
            '$match': {
                '_id': ObjectId(id_inventaris)
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
    data = aggregate_to_collection("inventaris", filter)
    # print("data1:", data)
    # print("testing")
    data = json.loads(bson.json_util.dumps(list(data)))
    # print("data2:", data)
    data = data[0]
    # print("data3:", data)
    if len(data)==0:
        raise Exception("Histori kajian tidak ditemukan")
    return data