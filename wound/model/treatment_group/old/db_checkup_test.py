import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
import bson,json

def create_checkup_test(request):
    check  = get_from_collection("patient_info",{"user_id":ObjectId(request.form["patient_id"])})
    check = json.loads(bson.json_util.dumps(list(check)))
    if len(check) == 0:
        raise Exception("Pasien tidak ditemukan")
    data = {
        "patient_id" : ObjectId(request.form["patient_id"])
    }
    nullable = {"blood_pressure":"string","pulse":"string","tension_level": "string","body_temperature":"float","body_temperature_unit": "string","abpi": "float","medical_history": "string"}
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
    data2 = {}
    nullable = {"aic":"float","fasting_blood_sugar": "string","glucose_tolerance": "string","random_blood_sugar":"string"}
    for param in nullable.keys():
        if request.form.get(param)!='""' and request.form.get(param)!="" and request.form.get(param)!="''" and request.form.get(param)!=None:
            if nullable[param]=="string":
                data2[param] = request.form[param]
            elif nullable[param]=="int":
                data2[param] = int(request.form[param])
            elif nullable[param]=="date":
                data2[param] = request.form[param]
            elif nullable[param]=="float":
                data2[param] = float(request.form[param])
        else:
            data2[param] = None
    data = insert_to_collection("checkup_test",data)
    data2["checkup_test_id"] = data.inserted_id
    data2 = insert_to_collection("diabetes_test",data2)
    return "Berhasil membuat pemeriksaan kesehatan baru"

def get_checkup_test_by_patient_id(patient_id):
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
            'from': 'diabetes_test', 
            'localField': '_id', 
            'foreignField': 'checkup_test_id', 
            'as': 'diabetes_test'
        }
    }]
    data = aggregate_to_collection("checkup_test",filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    if len(data)==0:
        raise Exception("Pasien ini tidak memiliki data pemeriksaan kesehatan")
    return data[0]