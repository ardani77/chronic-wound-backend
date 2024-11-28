from flask import Blueprint, request, Response
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
