from wound.model.db_setting import *
from flask import Request, Response
from bson import ObjectId
import json
from wound.helpers import image_h, directory_h
from werkzeug.utils import secure_filename
from pathlib import Path
from wound.model.treatment_group import db_wound_inspection_old

columns = ['_id', 'wound_inspection_id', 'parent_path', 'filename_no_ext', 'file_extension', 'original_url', 'thumb_url']

def _get_one_wound_image(id: ObjectId) -> pymongo.ReturnDocument:
    filters = {'_id': id}
    return get_one_from_collection("wound_image", filters=filters)

def create_wound_image(request: Request) -> Response:
    if not ObjectId.is_valid(request.form['wound_inspection_id']):
        return Response(response=json.dumps({'message': "Invalid Wound Inspection ID"}), status=400, mimetype="application/json")
    wound_inspection_response = db_wound_inspection_old.get_one_wound_inspection(request, id=request.form['wound_inspection_id'])
    if wound_inspection_response.status_code == 400:
        return wound_inspection_response
    image_file = request.files['image']
    if not image_file:
        return Response(response=json.dumps({'message': "Image file does not exist"}), status=400, mimetype="application/json")
    if not image_h.check_file(image_file.filename):
        return Response(response=json.dumps({'message': "Image file extension is not allowed"}), status=400, mimetype="application/json")
    else:
        filename = secure_filename(image_file.filename)
        image_file_parent_path = Path.joinpath(current_app.instance_path, current_app.config['UPLOAD_DIR']).joinpath("wound_images")
        filename = image_h.append_datetime(filename)
        directory_h.create_folder(image_file_parent_path)
        image_file.save(image_file_parent_path.joinpath(filename))
    filename_and_extension = image_h.separate_filename_and_ext(filename)
    data = {
        'parent_path': image_file_parent_path,
        'filename_no_ext': filename_and_extension[0],
        'file_extension': filename_and_extension[1],
        'original_url': image_file_parent_path.joinpath(filename),
        # TODO: create image thumb later
        'thumb_url': image_file_parent_path.joinpath(filename)
    }
    new_wound_image_id = insert_to_collection("wound_image", data).inserted_id
    document_result = _get_one_wound_image(new_wound_image_id)
    return Response(response=json.dumps(dict(document_result)), status=201, mimetype="application/json")

def get_all_wound_images(request: Request) -> Response:
    for query in request.args:
        if query not in columns:
            return Response(response=json.dumps({'message' : "Invalid query arguments"}), status=400, mimetype="application/json")
    cursor_result = get_from_collection("wound_image", filters=request.args)
    document_list = []
    for bson_document in cursor_result:
        document_list.append(dict(bson_document))
    return Response(response=json.dumps(document_list), status=200, mimetype="application/json")

def get_one_wound_image(request: Request, id: ObjectId) -> pymongo.ReturnDocument:
    document_result = _get_one_wound_image(id)
    if document_result is None:
        return Response(response=json.dumps({'message': "Invalid Wound History ID"}), status=400 , mimetype="application/json")
    return Response(response=json.dumps(document_result), status=200, mimetype="application/json")

