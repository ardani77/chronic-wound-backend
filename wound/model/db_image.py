import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
from wound.model.db_anotasi import *
from werkzeug.utils import secure_filename
import time
import os
from wound import utils

def get_image(filter = {}):
    collection = get_collection("image")
    row = collection.find(filter)
    return row

def insert_image(data):
    collection = get_collection("image")
    row = collection.insert_one(data)
    return row

def update_image(id, data):
    collection = get_collection("image")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_image(id):
    collection = get_collection("image")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_image(request):
    files = request.files["image"]
    if files and utils.allowed_file(files.filename):
        filename = secure_filename(files.filename)
        path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
        filename = utils.pad_timestamp(filename)
        try:
            os.makedirs(path)
        except OSError:
            pass
        id_anotasi = create_anotasi(request)
        filepath = os.path.join(path, filename)
        files.save(filepath)
        data = {
            "id_perawat": request.form["id_perawat"],
            "anotasi": id_anotasi,
            "filename": filename,
            "type": request.form["type"],
            "category": request.form["category"],
            "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
            "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
        }
        return insert_image(data).inserted_id
    else:
        raise Exception("Image not found or invalid extension")