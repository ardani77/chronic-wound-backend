import pymongo
import time
import json
from flask import Blueprint, request, Response
from flask import Flask, jsonify
from wound.model.db_user_roles import *
from wound.model.db_user_new import *



bp = Blueprint('auth-controller', __name__, url_prefix='/')

# daftar user baru
#bp.route('register-pasien', methods = ['POST'])
#def addPasien():
#    try:
#        data = {
#            "username": request.form["username"],
#            "email_user": request.form["email_user"],
#            "password_user": request.form["password_user"],
#            "noreg_pasien": request.form["noreg_pasien"],
#            "nama_pasien": request.form["nama_pasien"],
#            "no_handphone": int(request.form["no_handphone"]),
#            "alamat": request.form["alamat"],
#            "jenis_kelamin": request.form["jenis_kelamin"],
#            "usia": int(request.form["usia"]),
#            "tgl_lahir": int(request.form["tgl_lahir"]),
#            "agama_pasien": request.form["agama_pasien"],
#        }
#
#        cek = get_pasien(data)
#        
#        if cek == None:
#            row = create_pasien(data)
#            return Response(
#                response = json.dumps({"message" : "true"}),
#                mimetype = "application/json",
#                status   = 200
#                )
#        else:
#            return Response(
#                response = json.dumps({"message" : "false"}), 
#                mimetype="application/json", status=404
#                )                    
#    
#    except Exception as ex:
#        print(ex)
#        print(ex)
#        return Response(
#                response = json.dumps({"message" : f"{ex}"}), 
#                mimetype="application/json", status=500
#                )
#
## daftar perawat baru
#bp.route('register-perawat', methods = ['POST'])
#def createPerawat():
#    try:
#        data = {
#            "username": request.form["username"],
#            "email_user": request.form["email_user"],
#            "password_user": request.form["password_user"],
#            "nama_perawat": request.form["nama_perawat"],
#            "nip_perawat": request.form["nip_perawat"],
#        }
#        cek = get_perawat(data)
#            
#        if cek == None:
#            row = create_pasien(data)
#            return Response(
#                response = json.dumps({"message" : "true"}),
#                mimetype = "application/json",
#                status   = 200
#                )
#        else:
#            return Response(
#                response = json.dumps({"message" : "false"}), 
#                mimetype="application/json", status=404
#                ) 
#
#    except Exception as ex:
#        print(ex)
#        print(ex)
#        return Response(
#                response = json.dumps({"message" : f"{ex}"}), 
#                mimetype="application/json", status=500
#                )                  
    
@bp.route("v1/login",methods = ["POST"])
def login():
    try:
        data = get_one_from_collection("user",{"email": request.form["email"], "password": request.form["password"]})
        if data == None:
            raise Exception("User tidak ditemukan")
        data = get_one_user_roles({"user_id": ObjectId(data["_id"])})
        if data["role_healthcare_staff"]:
            return json.dumps({"message" : get_one_healthcare_staff_by_email(request) })
        elif data["role_patient"]:
            return json.dumps({"message" : get_one_patient_by_email(request) })
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)
    
    
#@bp.route("v1/logintest",methods = ["POST"])
#def logintest():
#    try:
#        data = get_one_from_collection("user",{"email": request.form["email"], "password": request.form["password"]})
#        # if not request.form["email"] or not request.form["password"]:
#        #     return jsonify({'success': False, 'message': 'Email dan kata sandi harus diisi'})
#        if data == None:
#            raise Exception("User tidak ditemukan")
#        
#        # Cari pengguna dengan email yang cocok
#        # pengguna = next((pengguna for pengguna in get_user if pengguna['email'] == request.form["email"]), None)
#
#        # if pengguna and pengguna['password'] == request.form["password"]:
#        #     return jsonify({'success': True, 'message': 'Login berhasil'})
#        # else:
#        #     data = get_one_user_roles({"user_id": ObjectId(data["_id"])})
#        #     return jsonify({'success': True, 'message': 'Login berhasil', 'roles': {key: value for key, value in data.items() if value is True})
#        data = get_one_user_roles({"user_id": ObjectId(data["_id"])})
#        if data["role_healthcare_staff"]:
#            return jsonify({'success': True, 'message': 'Login berhasil', 'user': get_one_healthcare_staff(request)})
#        elif data["role_patient"]:
#            return jsonify({'success': True, 'message': 'Login berhasil', 'user': get_one_patient(request)}) 
#    except Exception as ex:
#        print(ex)
#        return Response(response = json.dumps({"message" : f"{ex}"}), mimetype="application/json", status=500)