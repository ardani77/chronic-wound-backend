import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
from werkzeug.utils import secure_filename
import time

def get_anotasi(filter = {}):
    collection = get_collection("anotasi")
    row = collection.find(filter)
    return row

def insert_anotasi(data):
    collection = get_collection("anotasi")
    row = collection.insert_one(data)
    return row

def update_anotasi(id, data):
    collection = get_collection("anotasi")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_anotasi(id):
    collection = get_collection("anotasi")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_anotasi(request):
    data = {
        "anotasi_image": int(request.form["anotasi_image"]),
        "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
        "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
    }
    return insert_anotasi(data)