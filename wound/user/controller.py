import pymongo
from flask import Blueprint, request, Response, current_app
from wound.model import db_user_new
import json

bp = Blueprint('user-controller', __name__, url_prefix='/')

    
@bp.route("v1/patient", methods=["POST"])
def create_patient():
    try:
        return json.dumps({"message" : db_user_new.create_patient(request) })
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)

@bp.route("v1/healthcare_staff",methods=["POST"])
def create_healthcare_staff():
    try:
        return json.dumps({"message" : db_user_new.create_healthcare_staff(request) })
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/clinic_admin", methods=["POST"])
def create_clinic():
    try:
        return json.dumps({"message" : db_user_new.create_clinic_admin(request) })
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/healthcare_staff/<healthcare_staff_id>",methods=["GET"])
def get_one_healthcare_staff(healthcare_staff_id):
    try:
        return json.dumps( db_user_new.get_one_healthcare_staff(healthcare_staff_id) )
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    

@bp.route("v1/healthcare_staff/patient",methods=["PUT"])
def insert_patient_to_healthcare_staff():
    try:
        return json.dumps({"message" : db_user_new.insert_patient_to_healthcare_staff(request) })
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)

@bp.route("v1/patient",methods = ["GET"])
def get_all_patient():
    try:
        data = db_user_new.get_all_patient(request)
        return json.dumps(data)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/patient/<patient_id>")
def get_one_patient(patient_id):
    try:
        data = db_user_new.get_one_patient(patient_id)
        current_app.logger.error(data)
        return json.dumps(data)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)

#@bp.route("v1/patient/healthcare_staff/<healthcare_staff_id>",methods = ["GET"])
#def get_all_patient_by_healthcare_staff_id(healthcare_staff_id):
#    try:
#        return json.dumps(db_user_new.get_all_patient_by_healthcare_staff_id(healthcare_staff_id))
#    except Exception as ex:
#        print(ex)
#        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)

#@bp.route("v1/patient",methods=["GET"])
#def get_all_pasien():
#    try:
#       return db_user_new.get_all_patient(request)
#    except Exception as ex:
#        print(ex)
#        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
#    
#@bp.route("v1/perawat",methods=["GET"])
#def get_all_perawat():
#    try:
#       return db_user.get_all_perawat(request)
#    except Exception as ex:
#        print(ex)
#        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
#    return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)

