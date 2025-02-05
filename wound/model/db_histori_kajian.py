import json
import time
import bson
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *

def get_wound_history(filter = {}):
    collection = get_collection("wound_history")
    row = collection.find(filter)
    return row

def insert_wound_history(data):
    collection = get_collection("wound_history")
    row = collection.insert_one(data)
    return row

def update_wound_history(id, data):
    collection = get_collection("wound_history")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_wound_history(id):
    collection = get_collection("wound_history")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_wound_history(request):
    check  = get_from_collection("patient_info",{"user_id":ObjectId(request.form["patient_id"])})
    check = json.loads(bson.json_util.dumps(list(check)))
    if len(check) == 0:
        raise Exception("Pasien tidak ditemukan")
    check2  = get_from_collection("healthcare_staff_info",{"user_id":ObjectId(request.form["healthcare_staff_id"])})
    check2 = json.loads(bson.json_util.dumps(list(check2)))
    if len(check2) == 0:
        raise Exception("Perawat tidak ditemukan")
    check3  = get_from_collection("wound_inspection",{"_id":ObjectId(request.form["wound_inspection_id"])})
    check3 = json.loads(bson.json_util.dumps(list(check3)))
    if len(check3) == 0:
        raise Exception("Wound inspection tidak ditemukan")
    check4  = get_from_collection("tujuan_perawatan",{"_id":ObjectId(request.form["tujuan_perawatan_id"])})
    check4 = json.loads(bson.json_util.dumps(list(check4)))
    if len(check4) == 0:
        raise Exception("Tujuan perawatan tidak ditemukan")
    check5  = get_from_collection("medical_checkup",{"_id":ObjectId(request.form["medical_checkup_id"])})
    check5 = json.loads(bson.json_util.dumps(list(check5)))
    if len(check5) == 0:
        raise Exception("Medical checkup tidak ditemukan")
    check6  = get_from_collection("rekap_kunjungan",{"_id":ObjectId(request.form["rekap_kunjungan_id"])})
    check6 = json.loads(bson.json_util.dumps(list(check6)))
    if len(check6) == 0:
        raise Exception("Rekap kunjungan tidak ditemukan")
    data = {
               "patient_id": ObjectId(request.form["patient_id"]),
               "healthcare_staff_id": ObjectId(request.form["healthcare_staff_id"]),
               "wound_inspection_id": ObjectId(request.form["wound_inspection_id"]),
               "tujuan_perawatan_id": ObjectId(request.form["tujuan_perawatan_id"]),
               "medical_checkup_id": ObjectId(request.form["medical_checkup_id"]),
               "rekap_kunjungan_id": ObjectId(request.form["rekap_kunjungan_id"]),
               "created_at": time.strftime("%d/%m/%Y %H:%M:%S"),
               "updated_at": time.strftime("%d/%m/%Y %H:%M:%S")
           }
    insert_to_collection("wound_history", data)
    return "Berhasil input histori kajian baru"

def get_all_wound_history_by_patient_id(patient_id):
    check  = get_from_collection("patient_info",{"user_id":ObjectId(patient_id)})
    check = json.loads(bson.json_util.dumps(list(check)))
    if len(check) == 0:
        raise Exception("Pasien tidak ditemukan")
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
    data = aggregate_to_collection("wound_history", filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    if len(data)==0:
        raise Exception("Histori kajian tidak ditemukan")
    return data

def get_wound_history_by_id(id_wound_history):
    filter = [
        {
            '$match': {
                '_id': ObjectId(id_wound_history)
            }
        }, {
            '$lookup': {
                'from': 'wound_inspection', 
                'localField': 'wound_inspection_id', 
                'foreignField': '_id', 
                'as': 'wound_inspection', 
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'image', 
                            'localField': 'image_id', 
                            'foreignField': '_id', 
                            'as': 'image', 
                            'pipeline': [
                                {
                                    '$lookup': {
                                        'from': 'wound_annotation', 
                                        'localField': 'wound_annotation_id', 
                                        'foreignField': '_id', 
                                        'as': 'wound_annotation'
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }, {
            '$lookup': {
                'from': 'medical_checkup', 
                'localField': 'medical_checkup_id', 
                'foreignField': '_id', 
                'as': 'medical_checkup'
            }
        }, {
            '$lookup': {
                'from': 'tujuan_perawatan', 
                'localField': 'tujuan_perawatan_id', 
                'foreignField': '_id', 
                'as': 'tujuan_perawatan'
            }
        }, {
            '$lookup': {
                'from': 'rekap_kunjungan', 
                'localField': 'rekap_kunjungan_id', 
                'foreignField': '_id', 
                'as': 'rekap_kunjungan'
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
    data = aggregate_to_collection("wound_history", filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    data = data[0]
    if len(data)==0:
        raise Exception("Histori kajian tidak ditemukan")
    return data