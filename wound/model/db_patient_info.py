import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
import time,json,bson

def get_patient_info(filter = {}):
    collection = get_collection("patient_info")
    row = collection.find(filter)
    return row

def get_one_patient_info(filter):
    collection = get_collection("patient_info")
    row = collection.find_one(filter)
    return row

def aggregate_patient_info(filter):
    collection = get_collection("patient_info")
    row = collection.aggregate(filter)
    return row

def insert_patient_info(data):
    collection = get_collection("patient_info")
    row = collection.insert_one(data)
    return row

def update_patient_info(id, data):
    collection = get_collection("patient_info")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_patient_info(id):
    collection = get_collection("patient_info")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)