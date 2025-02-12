import pymongo
from flask import Blueprint, request, Response
from wound.model import db_inventaris, db_pemeriksaan,db_kajian, db_histori_kajian, db_rekap_kunjungan, db_treatment, db_tujuan_perawatan
import json

from wound.model.wound_group import db_wound_area

bp = Blueprint('keperawatan_luka-controller', __name__, url_prefix='/')

@bp.route("v1/medical_checkup",methods=["POST"])
def create_medical_checkup():
    try:
        return json.dumps({"medical_checkup_id" : str(db_pemeriksaan.create_medical_checkup(request)) })
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/medical_checkup/<id_medical_checkup>",methods=["GET"])
def get_medical_checkup_by_id(id_medical_checkup):
    try:
       return db_pemeriksaan.get_medical_checkup_by_id(id_medical_checkup)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/tambah-luka/", methods=["POST"])
def create_kajian_baru():
    try:
        return db_kajian.create_kajian_baru(request)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)

@bp.route("v1/histori_luka/<id_kajian>", methods=["GET"])
def get_kajian_baru_by_id(id_kajian):
    try:
        return db_kajian.get_kajian_baru_by_id(id_kajian)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/histori_kajian/<id_pasien>", methods=["GET"])
def get_kajian_baru_by_id_pasien(id_pasien):
    try:
        return db_kajian.get_kajian_baru_by_id_pasien(id_pasien)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/wound_history", methods=["POST"])
def create_wound_history():
    try:
        return json.dumps({"message" : str(db_histori_kajian.create_wound_history(request)) })
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/wound_history/patient/<patient_id>", methods=["GET"])
def get_all_wound_history_by_patient_id(patient_id):
    try:
        return db_histori_kajian.get_all_wound_history_by_patient_id(patient_id)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/wound_history/<id_wound_history>", methods=["GET"])
def get_wound_history_by_id(id_wound_history):
    try:
        return db_histori_kajian.get_wound_history_by_id(id_wound_history)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/treatment/", methods=["POST"])
def create_treatment():
    try:
        return db_treatment.create_treatment(request)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/treatment/<id_treatment>", methods=["GET"])
def get_treatment_by_id(id_treatment):
    try:
        return db_treatment.get_treatment_by_id(id_treatment)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/tujuan_perawatan", methods=["POST"])
def create_tujuan_perawatan():
    try:
        return json.dumps({"tujuan_perawatan_id" : str(db_tujuan_perawatan.create_tujuan_perawatan(request)) })
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/tujuan_perawatan/<id_tujuan_perawatan>", methods=["GET"])
def get_tujuan_perawatan_by_id(id_tujuan_perawatan):
    try:
        return db_tujuan_perawatan.get_tujuan_perawatan_by_id(id_tujuan_perawatan)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/inventaris", methods=["POST"])
def create_inventaris():
    try:
        return json.dumps({"inventaris_id" : str(db_inventaris.create_inventaris(request)) })
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/inventaris/<id_inventaris>", methods=["GET"])
def get_inventaris_by_id(id_inventaris):
    try:
        return db_inventaris.get_inventaris_by_id(id_inventaris)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/rekap_kunjungan", methods=["POST"])
def create_rekap_kunjungan():
    try:
        return json.dumps({"rekap_kunjungan_id" : str(db_rekap_kunjungan.create_rekap_kunjungan(request)) })
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/rekap_kunjungan/<id_rekap_kunjungan>", methods=["GET"])
def get_rekap_kunjungan_by_id(id_rekap_kunjungan):
    try:
        return db_rekap_kunjungan.get_rekap_kunjungan_by_id(id_rekap_kunjungan)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/rekap_kunjungan/patient/<patient_id>", methods=["GET"])
def get_rekap_kunjungan_by_patient_id(patient_id):
    try:
        return db_rekap_kunjungan.get_rekap_kunjungan_by_patient_id(patient_id)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/wound_area/<id_wound_area>", methods=["GET"])
def get_wound_area_by_id(id_wound_area):
    try:
        return db_wound_area.get_wound_area_by_id(id_wound_area)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/wound_area/", methods=["POST"])
def create_wound_area():
    try:
        return db_wound_area.create_wound_area(request)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/wound_area/", methods=["GET"])
def get_all_wound_area():
    try:
        return db_wound_area.get_all_wound_area()
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)