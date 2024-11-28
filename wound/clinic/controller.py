import pymongo
from flask import Blueprint, request, Response
from wound.model import db_clinic
import json

bp = Blueprint('clinic-controller', __name__, url_prefix='/')

@bp.route("v1/clinic", methods=["POST"])
def create_clinic():
    try:
        return json.dumps({"message" : db_clinic.create_clinic(request) })
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)