import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
import time,json,bson

def get_clinic_admin_info(filter = {}):
    collection = get_collection("clinic_admin_info")
    row = collection.find(filter)
    return row

def get_one_clinic_admin_info(filter):
    collection = get_collection("clinic_admin_info")
    row = collection.find_one(filter)
    return row

def aggregate_clinic_admin_info(filter):
    collection = get_collection("clinic_admin_info")
    row = collection.aggregate(filter)
    return row

def insert_clinic_admin_info(data):
    collection = get_collection("clinic_admin_info")
    row = collection.insert_one(data)
    return row

def update_clinic_admin_info(id, data):
    collection = get_collection("clinic_admin_info")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_clinic_admin_info(id):
    collection = get_collection("clinic_admin_info")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)