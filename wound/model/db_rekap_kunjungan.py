import json
import time
import bson
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *

def get_rekap_kunjungan(filter = {}):
    collection = get_collection("rekap_kunjungan")
    row = collection.find(filter)
    return row

def insert_rekap_kunjungan(data):
    collection = get_collection("rekap_kunjungan")
    row = collection.insert_one(data)
    return row

def update_rekap_kunjungan(id, data):
    collection = get_collection("rekap_kunjungan")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_rekap_kunjungan(id):
    collection = get_collection("rekap_kunjungan")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_rekap_kunjungan(request):
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
    nullable = {"hasil_pemeriksaan": "string",
               "keterangan": "string",
               "kunjungan": "string"}
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
    data = insert_rekap_kunjungan(data)
    return data.inserted_id

def get_rekap_kunjungan_by_id(id_rekap_kunjungan):
    filter = [
        {
            '$match': {
                '_id': ObjectId(id_rekap_kunjungan)
            }
        }, {
            '$lookup': {
                'from': 'user', 
                'localField': 'patient_id', 
                'foreignField': '_id', 
                'as': 'patient', 
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'patient_info', 
                            'localField': '_id', 
                            'foreignField': 'user_id', 
                            'as': 'patient_info', 
                            'pipeline': [
                                {
                                    '$project': {
                                        '_id': 0, 
                                        'registration_id': 1
                                    }
                                }
                            ]
                        }
                    }, {
                        '$project': {
                            '_id': 0, 
                            'name': 1, 
                            'patient_info': 1
                        }
                    }
                ]
            }
        }, {
            '$lookup': {
                'from': 'user', 
                'localField': 'healthcare_staff_id', 
                'foreignField': '_id', 
                'as': 'healthcare_staff', 
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'healthcare_staff_info', 
                            'localField': '_id', 
                            'foreignField': 'user_id', 
                            'as': 'healthcare_staff_info', 
                            'pipeline': [
                                {
                                    '$project': {
                                        '_id': 0, 
                                        'nip': 1
                                    }
                                }
                            ]
                        }
                    }, {
                        '$project': {
                            '_id': 0, 
                            'name': 1, 
                            'healthcare_staff_info': 1
                        }
                    }
                ]
            }
        }
    ]
    data = aggregate_to_collection("rekap_kunjungan", filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    data = data[0]
    if len(data)==0:
        raise Exception("Pemeriksaan kesehatan tidak ditemukan")
    return data

def get_rekap_kunjungan_by_patient_id(patient_id):
    filter = [
        {
            '$match': {
                'patient_id': ObjectId(patient_id)
            }
        }, {
            '$lookup': {
                'from': 'user', 
                'localField': 'healthcare_staff_id', 
                'foreignField': '_id', 
                'as': 'healthcare_staff', 
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'healthcare_staff_info', 
                            'localField': '_id', 
                            'foreignField': 'user_id', 
                            'as': 'healthcare_staff_info', 
                            'pipeline': [
                                {
                                    '$project': {
                                        '_id': 0, 
                                        'nip': 1
                                    }
                                }
                            ]
                        }
                    }, {
                        '$project': {
                            '_id': 0, 
                            'name': 1, 
                            'healthcare_staff_info': 1
                        }
                    }
                ]
            }
        }
    ]
    data = aggregate_to_collection("rekap_kunjungan", filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    if len(data)==0:
        raise Exception("Pemeriksaan kesehatan tidak ditemukan")
    return data