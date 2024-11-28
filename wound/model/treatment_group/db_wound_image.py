import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
from wound.model.treatment_group.db_wound_annotation import *
from werkzeug.utils import secure_filename
import time, os, bson, json
from wound import utils
import base64

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
        filepath = os.path.join(path, filename)
        files.save(filepath)
        id_anotasi = create_annotation(filepath,request).inserted_id
        filename_no_ext = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        data = {
            "parent_path": path,
            "filename_no_ext": filename_no_ext,
            "file_extension": extension,
            "wound_annotation_id": id_anotasi,
            "original_url": filepath, 
            "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
            "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
        }
        data = insert_to_collection("image",data)
        return data.inserted_id
    else:
        raise Exception("Image not found or invalid extension")
    
def get_image_by_id(image_id):
    filter = [
    {
        '$match': {
            '_id': ObjectId(image_id)
        }
    }, {
        '$lookup': {
            'from': 'wound_annotation', 
            'localField': 'wound_annotation_id', 
            'foreignField': '_id', 
            'as': 'wound_annotation'
        }
    }, {
        '$project': {
            'wound_annotation_id': 0
        }
    }]
    data = aggregate_to_collection("image",filter)
    data = json.loads(bson.json_util.dumps(list(data)))[0]
    print(data["original_url"])
    with open(data["original_url"], "rb") as img_file:
            data["image"] = str(base64.b64encode(img_file.read()).decode("utf-8"))
    return data
