import json
import time
import bson
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *

def get_medical_checkup(filter = {}):
    collection = get_collection("medical_checkup")
    row = collection.find(filter)
    return row

def insert_medical_checkup(data):
    collection = get_collection("medical_checkup")
    row = collection.insert_one(data)
    return row

def update_medical_checkup(id, data):
    collection = get_collection("medical_checkup")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_medical_checkup(id):
    collection = get_collection("medical_checkup")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_medical_checkup(request):
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
    data = {
        "patient_id" : ObjectId(request.form["patient_id"]),
        "healthcare_staff_id" : ObjectId(request.form["healthcare_staff_id"]), 
        "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
        "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S")
    }
    nullable = {"tipe_luka": "string",
               "tipe_penyembuhan": "string",
               "tekanan_darah": "string",
               "nadi": "string",
               "prehipertensi": "string",
               "suhu": "string",
               "gula_darah_sewaktu": "string",
               "abpi": "string",
               "riwayat_kajian_luka": "string"}
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
    data = insert_medical_checkup(data)
    return data.inserted_id

def get_medical_checkup_by_id(id_medical_checkup):
    filter = [
        {
            '$match': {
                '_id': ObjectId(id_medical_checkup)
            }
        }, {
            '$lookup': {
                'from': 'medical_checkup', 
                'localField': 'id_medical_checkup', 
                'foreignField': '_id', 
                'as': 'medical_checkup'
            }
        }
    ]
    # print(filter)
    data = aggregate_to_collection("medical_checkup", filter)
    # print("data1:", data)
    # print("testing")
    data = json.loads(bson.json_util.dumps(list(data)))
    # print("data2:", data)
    data = data[0]
    # print("data3:", data)
    if len(data)==0:
        raise Exception("Pemeriksaan kesehatan tidak ditemukan")
    return data