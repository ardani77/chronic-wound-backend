import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *

def get_pemeriksaan_kesehatan(filter = {}):
    collection = get_collection("pemeriksaan_kesehatan")
    row = collection.find(filter)
    return row

def insert_pemeriksaan_kesehatan(data):
    collection = get_collection("pemeriksaan_kesehatan")
    row = collection.insert_one(data)
    return row

def update_pemeriksaan_kesehatan(id, data):
    collection = get_collection("pemeriksaan_kesehatan")
    id=ObjectId(id)
    filter = {"_id":id}
    return collection.update_one(filter, data, upsert=False)

def delete_pemeriksaan_kesehatan(id):
    collection = get_collection("pemeriksaan_kesehatan")
    id = ObjectId(id)
    filter = {"_id":id}
    return collection.delete_one(filter)

def create_pemeriksaan_kesehatan(request):
    data = {
               "id_perawat": int(request.form["id_perawat"]),
               "id_pasien": int(request.form["id_pasien"]),
               "tipe_luka": int(request.form["tipe_luka"]),
               "tipe_penyembuhan": request.form["tipe_penyembuhan"],
               "tekanan_darah": int(request.form["tekanan_darah"]),
               "nadi": int(request.form["nadi"]),
               "prehipertensi": int(request.form["prehipertensi"]),
               "suhu": int(request.form["suhu"]),
               "gula_darah_sewaktu": int(request.form["gula_darah_sewaktu"]),
               "abpi": int(request.form["abpi"]),
               "riwayat_kajian_luka": request.form["riwayat_kajian_luka"]
           }
    row = insert_pemeriksaan_kesehatan(data)
    return "Berhasil input pemeriksaan kesehatan baru"