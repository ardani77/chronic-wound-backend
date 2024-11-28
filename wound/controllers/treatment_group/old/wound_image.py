from flask import Blueprint, request, Response
from wound.model.treatment_group import db_wound_image
import json, bson

bp = Blueprint('wound-image-controller', __name__)

@bp.route("/wound_image", methods=["POST"])
def create_wound_image() -> bson.ObjectId :
    try:
       return db_wound_image.create_wound_image(request)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")
    
@bp.route("/wound_image", methods=["GET"])
def find_all_wound_images():
    try:
       return db_wound_image.get_all_wound_images(request)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")

@bp.route("/wound_image/<id>", methods=["GET"])
def find_one_wound_image(id: str):
    if not bson.ObjectId.is_valid(id):
        return Response(response = json.dumps({'message' : "Invalid Wound Inspection ID"}), status=400, mimetype="application/json")
    try:
       return db_wound_image.get_one_wound_image(request, id)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({'message' : f"{ex}"}), status=500, mimetype="application/json")