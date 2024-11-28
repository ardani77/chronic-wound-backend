import pymongo
from flask import Blueprint, request, Response
from wound.model import db_pemeriksaan,db_kajian, db_histori_kajian
import json

bp = Blueprint('keperawatan_luka-controller', __name__, url_prefix='/')

@bp.route("v1/pemeriksaan-kesehatan/",methods=["POST"])
def create_pemeriksaan_kesehatan():
    try:
       return db_pemeriksaan.create_pemeriksaan_kesehatan(request)
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
    
@bp.route("v1/histori_luka/", methods=["POST"])
def create_histori_luka():
    try:
        return db_histori_kajian.create_histori_kajian(request)
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)