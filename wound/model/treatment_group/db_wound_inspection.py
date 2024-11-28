import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
import bson,json

def create_wound_inspection(request):
    check  = get_from_collection("patient_info",{"user_id":ObjectId(request.form["patient_id"])})
    check = json.loads(bson.json_util.dumps(list(check)))
    if len(check) == 0:
        raise Exception("Pasien tidak ditemukan")
    data = {
        "patient_id" : ObjectId(request.form["patient_id"])
    }
    check2 = get_from_collection("image",{"_id": ObjectId(request.form["image_id"])})
    check2 = json.loads(bson.json_util.dumps(list(check2)))
    if len(check2) == 0:
        raise Exception("Image tidak ditemukan")
    check2=check2[0]
    nullable = {"wound_area_score":"string", "wound_depth_score":"string", "wound_edge_score": "string", "wound_undermining_score": "string", "wound_necrotic_type_score": "string","wound_necrotic_amount_score":"string","wound_exudate_type_score":"string","wound_exudate_amount_score":"string","wound_surrounding_skin_score":"string","wound_peripheral_edema_score":"string","wound_peripheral_induration_score":"string","wound_granulation_score":"string","wound_epithelialization_score":"string"}
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
    data["image_id"] = []
    data["image_id"].append(ObjectId(check2["_id"]["$oid"]))
    insert_to_collection("wound_inspection",data)
    return "Berhasil menambah kajian baru"

def get_wound_inspection_by_patient_id(patient_id):
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
            'from': 'image', 
            'localField': 'image_id', 
            'foreignField': '_id', 
            'pipeline': [
                {
                    '$lookup': {
                        'from': 'wound_annotation', 
                        'localField': 'wound_annotation_id', 
                        'foreignField': '_id', 
                        'as': 'wound_annotation'
                    }
                }
            ], 
            'as': 'image'
        }
    }]
    data = aggregate_to_collection("wound_inspection",filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    if len(data)==0:
        raise Exception("User ini tidak memiliki kajian luka")
    return data

def get_wound_inspection_by_id(wound_inspection_id):
    filter = [
    {
        '$match': {
            '_id': ObjectId(wound_inspection_id)
        }
    }, {
        '$lookup': {
            'from': 'image', 
            'localField': 'image_id', 
            'foreignField': '_id', 
            'pipeline': [
                {
                    '$lookup': {
                        'from': 'wound_annotation', 
                        'localField': 'wound_annotation_id', 
                        'foreignField': '_id', 
                        'as': 'wound_annotation'
                    }
                }
            ], 
            'as': 'image'
        }
    }]
    data = aggregate_to_collection("wound_inspection",filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    if len(data)==0:
        raise Exception("Kajian luka tidak ditemukan")
    return data