import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
import time,json,bson

def get_healthcare_staff_info(filter = {}):
    collection = get_collection("healthcare_staff_info")
    row = collection.find(filter)
    return row

def get_one_healthcare_staff_info(filter):
    collection = get_collection("healthcare_staff_info")
    row = collection.find_one(filter)
    return row

def aggregate_healthcare_staff_info(filter):
    collection = get_collection("healthcare_staff_info")
    row = collection.aggregate(filter)
    return row

def insert_healthcare_staff_info(data):
    collection = get_collection("healthcare_staff_info")
    row = collection.insert_one(data)
    return row

def update_healthcare_staff_info(id, data):
    collection = get_collection("healthcare_staff_info")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_healthcare_staff_info(id):
    collection = get_collection("healthcare_staff_info")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)