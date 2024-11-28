import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
import time,json,bson

def get_user_roles(filter = {}):
    collection = get_collection("user_roles")
    row = collection.find(filter)
    return row

def get_one_user_roles(filter):
    collection = get_collection("user_roles")
    row = collection.find_one(filter)
    return row

def aggregate_user_roles(filter):
    collection = get_collection("user_roles")
    row = collection.aggregate(filter)
    return row

def insert_user_roles(data):
    collection = get_collection("user_roles")
    row = collection.insert_one(data)
    return row

def update_user_roles(id, data):
    collection = get_collection("user_roles")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_user_roles(id):
    collection = get_collection("user_roles")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)