import json
import time
import bson
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *

def get_tujuan_perawatan(filter = {}):
    collection = get_collection("tujuan_perawatan")
    row = collection.find(filter)
    return row

def insert_tujuan_perawatan(data):
    collection = get_collection("tujuan_perawatan")
    row = collection.insert_one(data)
    return row

# def update_tujuan_perawatan(id, data):
#     collection = get_collection("tujuan_perawatan")
#     id=ObjectId(id)
#     filter = {"_id":id}
#     return collection.update_one(filter, data, upsert=False)

def delete_tujuan_perawatan(id):
    collection = get_collection("tujuan_perawatan")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_tujuan_perawatan(request):
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
    nullable = {"tindakan_keperawatan": "list",
               "evaluasi": "string",
               "rencana_tindakan_lanjutan": "string",
               "notes": "string"}
    for param in nullable.keys():
        if request.form.get(param)!='""' and request.form.get(param)!="" and request.form.get(param)!="''" and request.form.get(param)!=None:
            if nullable[param]=="string":
                data[param] = request.form[param]
            elif nullable[param]=="int":
                data[param] = int(request.form[param])
            elif nullable[param]=="float":
                data[param] = request.form[param]
            elif nullable[param] == "list":
                try:
                    # Parsing JSON ke list
                    data[param] = json.loads(request.form[param])  # Parsing JSON ke list
                    # Verifikasi bahwa data adalah list dan semua elemen dalam list adalah string
                    if not isinstance(data[param], list):
                        raise Exception(f"Format {param} harus berupa array (list) JSON")
                    for item in data[param]:
                        if not isinstance(item, str):
                            raise Exception(f"Semua elemen dalam {param} harus berupa string")
                except json.JSONDecodeError:
                    raise Exception(f"Format {param} harus berupa array JSON yang valid")
        else:
            data[param] = None
    # data = {
    #     "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
    #     "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
    # }
    data = insert_tujuan_perawatan(data)
    return data.inserted_id

def get_tujuan_perawatan_by_id(tujuan_perawatan_id):
    filter = [
    {
        '$match': {
            '_id': ObjectId(tujuan_perawatan_id)
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
    data = aggregate_to_collection("tujuan_perawatan",filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    if len(data)==0:
        raise Exception("Histori kajian tidak ditemukan")
    return data

def update_tujuan_perawatan(id, data):
    collection = get_collection("tujuan_perawatan")
    id = ObjectId(id)
    filter = {"_id": id}
    
    if "tindakan_keperawatan" in data and isinstance(data["tindakan_keperawatan"], str):
        try:
            data["tindakan_keperawatan"] = json.loads(data["tindakan_keperawatan"])
        except json.JSONDecodeError:
            raise Exception("Format tindakan_keperawatan harus berupa array JSON")
    
    return collection.update_one(filter, {"$set": data}, upsert=False)
