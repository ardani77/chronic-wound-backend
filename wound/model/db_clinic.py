import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
import time,json,bson

def get_clinic(filter = {}):
    collection = get_collection("clinic")
    row = collection.find(filter)
    return row

def get_one_clinic(filter):
    collection = get_collection("clinic")
    row = collection.find_one(filter)
    return row

def aggregate_clinic(filter):
    collection = get_collection("clinic")
    row = collection.aggregate(filter)
    return row

def insert_clinic(data):
    collection = get_collection("clinic")
    row = collection.insert_one(data)
    return row

def update_clinic(id, data):
    collection = get_collection("clinic")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_clinic(id):
    collection = get_collection("clinic")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_clinic(request):
    # data = {
    #     "name": request.form["name"],
    #     "display_name": request.form["display_name"],
    #     "clinic_quota": request.form["clinic_quota"],
    #     "updated_at": time.strftime("%d/%m/%Y %H:%M:%S"),
    #     "created_at": time.strftime("%d/%m/%Y %H:%M:%S"),
    # }
    if request.form.get("registration_id")!='""' and request.form.get("registration_id")!="" and request.form.get("registration_id")!="''" and request.form.get("registration_id")!=None:
        pass
    else:
        raise Exception("registration_id tidak ada")
    # check = get_from_collection("user",{"email":request.form["email"]})
    # check = json.loads(bson.json_util.dumps(list(check))) 
    # if len(check) !=0:
    #     raise Exception("email yang dimasukkan telah digunakan")
    # nullable = {"name":"string","phone_number": "string","address":"string","gender":"string","religion":"string","date_of_birth":"date"}
    # for param in nullable.keys():
    #     if request.form.get(param)!='""' and request.form.get(param)!="" and request.form.get(param)!="''" and request.form.get(param)!=None:
    #         if nullable[param]=="string":
    #             data[param] = request.form[param]
    #         elif nullable[param]=="int":
    #             data[param] = int(request.form[param])
    #         elif nullable[param]=="date":
    #             data[param] = request.form[param]
    #     else:
    #         data[param] = None
    # user_id = insert_to_collection("user",data).inserted_id
    # data = {
    #     "user_id": user_id,
    #     "role_patient" : False,
    #     "role_healthcare_staff": False,
    #     "role_clinic_admin": True,
    #     "role_server_admin": False,
    # }
    # insert_to_collection("user_roles",data)
    data = {
        # "user_id": user_id,
        "name": request.form["name"],
        "display_name": request.form["display_name"],
        "clinic_quota": request.form["clinic_quota"],
        "updated_at": time.strftime("%d/%m/%Y %H:%M:%S"),
        "created_at": time.strftime("%d/%m/%Y %H:%M:%S"),
        "registration_id": request.form["registration_id"]
        }
    insert_to_collection("clinic",data)
    return "Berhasil menambahkan clinic baru"