import pymongo
from flask import Blueprint, request, Response
from wound.model import db_pemeriksaan,db_kajian, db_histori_kajian, db_treatment, db_tujuan_perawatan
import json

from wound.model.wound_group import db_wound_area

bp = Blueprint('keperawatan_luka-controller', __name__, url_prefix='/')

@bp.route("v1/pemeriksaan-kesehatan/",methods=["POST"])
def create_pemeriksaan_kesehatan():
    try:
       return db_pemeriksaan.create_pemeriksaan_kesehatan(request)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/pemeriksaan-kesehatan/<id_pemeriksaan_kesehatan>",methods=["GET"])
def get_pemeriksaan_kesehatan_by_id(id_pemeriksaan_kesehatan):
    try:
       return db_pemeriksaan.get_pemeriksaan_kesehatan_by_id(id_pemeriksaan_kesehatan)
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
    
@bp.route("v1/wound_history/", methods=["POST"])
def create_wound_history():
    try:
        return db_histori_kajian.create_histori_kajian(request)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
@bp.route("v1/wound_history/<id_wound_history>", methods=["GET"])
def get_wound_history_by_id(id_wound_history):
    try:
        return db_histori_kajian.get_histori_kajian_by_id(id_wound_history)
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
    
@bp.route("v1/tujuan_perawatan/", methods=["POST"])
def create_tujuan_perawatan():
    try:
        return db_tujuan_perawatan.create_tujuan_perawatan(request)
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