import time
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

def update_tujuan_perawatan(id, data):
    collection = get_collection("tujuan_perawatan")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_tujuan_perawatan(id):
    collection = get_collection("tujuan_perawatan")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_tujuan_perawatan(request):
    data = {
               "healthcarestaff_id": int(request.form["healthcarestaff_id"]),
               "patient_id": int(request.form["patient_id"]),
               "tindakan_keperawatan": request.form["tindakan_keperawatan"],
               "evaluasi": request.form["evaluasi"],
               "rencana_tindakan_lanjutan": request.form["rencana_tindakan_lanjutan"],
               "notes": request.form["notes"],
               "created_at": time.strftime("%d/%m/%Y %H:%M:%S")
           }
    insert_to_collection("tujuan_perawatan", data)
    return "Berhasil input tujuan perawatan baru"

