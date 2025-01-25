import os
from flask import Blueprint, current_app, jsonify, request, Response, send_file, send_from_directory, url_for
from wound.model.treatment_group import db_wound_image
import json, bson

bp = Blueprint('wound-image-controller', __name__)

@bp.route("/image",methods = ["POST"])
def create_image():
    try:
        return json.dumps({"message" : str(db_wound_image.create_image(request)) })
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)

@bp.route("/image/<image_id>",methods=["GET"])
def get_image_by_id(image_id):
    try:
        return json.dumps(db_wound_image.get_image_by_id(image_id) )
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("/view_image/<image_id>",methods=["GET"])
def tampilkan_image_by_id(image_id):
    try:
        imageView = db_wound_image.get_image_by_id(image_id)
        path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
        print('imageView')
        return send_from_directory(path, imageView['filename_no_ext']+imageView['file_extension'], mimetype="image/jpeg")
    except Exception as ex:
        print(ex.args)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)

@bp.route("/image_url/<id_image>",methods=["GET"])
def tampilkan_image(id_image):
    try:
        image_url = url_for('wound-image-controller.tampilkan_image_by_id', image_id=id_image, _external=True)
        print('imageView')
        return json.dumps({"image_url" : str(image_url) })
    except Exception as ex:
        print(ex.args)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)