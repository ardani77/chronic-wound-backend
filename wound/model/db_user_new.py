import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
from wound.model.db_patient_info import *
from wound.model.db_healthcare_staff_info import *
from wound.model.db_user_roles import *
import time,json,bson
from datetime import datetime

def create_patient(request):
    data = {
        "email": request.form["email"],
        "password": request.form["password"],
        "updated_at": time.strftime("%d/%m/%Y %H:%M:%S"),
        "created_at": time.strftime("%d/%m/%Y %H:%M:%S"),
    }
    if request.form.get("registration_id")!='""' and request.form.get("registration_id")!="" and request.form.get("registration_id")!="''" and request.form.get("registration_id")!=None:
        pass
    else:
        raise Exception("id registrasi tidak ada")
    check = get_from_collection("user",{"email":request.form["email"]})
    check = json.loads(bson.json_util.dumps(list(check)))
    if len(check) !=0:
        raise Exception("email yang dimasukkan telah digunakan")
    nullable = {"name":"string","phone_number": "string","address":"string","gender":"string","religion":"string","date_of_birth":"date"}
    for param in nullable.keys():
        if request.form.get(param)!='""' and request.form.get(param)!="" and request.form.get(param)!="''" and request.form.get(param)!=None:
            if nullable[param]=="string":
                data[param] = request.form[param]
            elif nullable[param]=="int":
                data[param] = int(request.form[param])
            elif nullable[param]=="date":
                data[param] = request.form[param]
        else:
            data[param] = None
    user_id = insert_to_collection("user",data).inserted_id
    data = {
        "user_id": user_id,
        "role_patient" : True,
        "role_healthcare_staff": False,
        "role_clinic_admin": False,
        "role_server_admin": False,
    }
    insert_to_collection("user_roles", data)
    data = {
        "user_id": user_id,
        "registration_id": request.form["registration_id"],
        "healthcare_staff_id": [],
        }
    insert_to_collection("patient_info", data)
    return "Berhasil menambahkan pasien baru"

def create_healthcare_staff(request):
    data = {
        "email": request.form["email"],
        "password": request.form["password"],
        "updated_at": time.strftime("%d/%m/%Y %H:%M:%S"),
        "created_at": time.strftime("%d/%m/%Y %H:%M:%S"),
    }
    if request.form.get("nip")!='""' and request.form.get("nip")!="" and request.form.get("nip")!="''" and request.form.get("nip")!=None:
        pass
    else:
        raise Exception("nip tidak ada")
    check = get_from_collection("user",{"email":request.form["email"]})
    check = json.loads(bson.json_util.dumps(list(check))) 
    if len(check) !=0:
        raise Exception("email yang dimasukkan telah digunakan")
    nullable = {"name":"string","phone_number": "string","address":"string","gender":"string","religion":"string","date_of_birth":"date"}
    for param in nullable.keys():
        if request.form.get(param)!='""' and request.form.get(param)!="" and request.form.get(param)!="''" and request.form.get(param)!=None:
            if nullable[param]=="string":
                data[param] = request.form[param]
            elif nullable[param]=="int":
                data[param] = int(request.form[param])
            elif nullable[param]=="date":
                data[param] = request.form[param]
        else:
            data[param] = None
    user_id = insert_to_collection("user",data).inserted_id
    data = {
        "user_id": user_id,
        "role_patient" : False,
        "role_healthcare_staff": True,
        "role_clinic_admin": False,
        "role_server_admin": False,
    }
    insert_to_collection("user_roles",data)
    data = {
        "user_id": user_id,
        "nip": request.form["nip"],
        "patient_id": [],
        }
    insert_to_collection("healthcare_staff_info",data)
    return "Berhasil menambahkan perawat baru"

def create_clinic_admin(request):
    data = {
        "email": request.form["email"],
        "password": request.form["password"],
        "updated_at": time.strftime("%d/%m/%Y %H:%M:%S"),
        "created_at": time.strftime("%d/%m/%Y %H:%M:%S"),
    }
    if request.form.get("nip")!='""' and request.form.get("nip")!="" and request.form.get("nip")!="''" and request.form.get("nip")!=None:
        pass
    else:
        raise Exception("nip tidak ada")
    check = get_from_collection("user",{"email":request.form["email"]})
    check = json.loads(bson.json_util.dumps(list(check))) 
    if len(check) !=0:
        raise Exception("email yang dimasukkan telah digunakan")
    nullable = {"name":"string","phone_number": "string","address":"string","gender":"string","religion":"string","date_of_birth":"date"}
    for param in nullable.keys():
        if request.form.get(param)!='""' and request.form.get(param)!="" and request.form.get(param)!="''" and request.form.get(param)!=None:
            if nullable[param]=="string":
                data[param] = request.form[param]
            elif nullable[param]=="int":
                data[param] = int(request.form[param])
            elif nullable[param]=="date":
                data[param] = request.form[param]
        else:
            data[param] = None
    user_id = insert_to_collection("user",data).inserted_id
    data = {
        "user_id": user_id,
        "role_patient" : False,
        "role_healthcare_staff": False,
        "role_clinic_admin": True,
        "role_server_admin": False,
    }
    insert_to_collection("user_roles",data)
    data = {
        "user_id": user_id,
        "nip": request.form["nip"]
        }
    insert_to_collection("clinic_admin_info",data)
    return "Berhasil menambahkan admin baru"

def get_one_healthcare_staff_by_email(request):
    filter = [
    {
        '$match': {
            'email': request.form["email"], 
            'password': request.form["password"]
        }
    }, {
        '$lookup': {
            'from': 'healthcare_staff_info', 
            'localField': '_id', 
            'foreignField': 'user_id', 
            'as': 'healthcare_staff_info'
        }
    }, {
        '$addFields': {
            'roles': 'perawat'
        }
    },
    {
        '$addFields': {
            'usia': {
                '$cond': {
                    'if': {
                        '$ne': [
                            '$date_of_birth', None
                        ]
                    }, 
                    'then': {
                        '$floor': {
                            '$divide': [
                                {
                                    '$subtract': [
                                        {
                                            '$toDate': datetime.utcnow()
                                        }, {
                                            '$toDate': '$date_of_birth'
                                        }
                                    ]
                                }, 31536000000
                            ]
                        }
                    }, 
                    'else': None
                }
            }
        }
    }]
    data = aggregate_to_collection("user",filter)
    # print("test")
    print(data)
    data = json.loads(bson.json_util.dumps(list(data)))
    data = data[0]
    return data

def get_one_patient_by_email(request):
    filter = [
    {
        '$match': {
            'email': request.form["email"], 
            'password': request.form["password"]
        }
    }, {
        '$lookup': {
            'from': 'patient_info', 
            'localField': '_id', 
            'foreignField': 'user_id', 
            'as': 'patient_info'
        }
    }, {
        '$addFields': {
            'roles': 'pasien'
        }
    },
    {
        '$addFields': {
            'usia': {
                '$cond': {
                    'if': {
                        '$ne': [
                            '$date_of_birth', None
                        ]
                    }, 
                    'then': {
                        '$floor': {
                            '$divide': [
                                {
                                    '$subtract': [
                                        {
                                            '$toDate': datetime.utcnow()
                                        }, {
                                            '$toDate': '$date_of_birth'
                                        }
                                    ]
                                }, 31536000000
                            ]
                        }
                    }, 
                    'else': None
                }
            }
        }
    }]
    data = aggregate_to_collection("user",filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    data = data[0]
    return data

def get_all_patient(request):
    filter = [
    {
        '$lookup': {
            'from': 'user_roles', 
            'localField': '_id', 
            'foreignField': 'user_id', 
            'as': 'user_roles'
        }
    }, {
        '$match': {
            'user_roles': {
                '$elemMatch': {
                    'role_patient': True
                }
            }
        }
    }, {
        '$lookup': {
            'from': 'patient_info', 
            'localField': '_id', 
            'foreignField': 'user_id', 
            'as': 'patient_info'
        }
    }, {
        '$project': {
            'user_roles': 0
        }
    }, {
        '$addFields': {
            'usia': {
                '$cond': {
                    'if': {
                        '$ne': [
                            '$date_of_birth', None
                        ]
                    }, 
                    'then': {
                        '$floor': {
                            '$divide': [
                                {
                                    '$subtract': [
                                        {
                                            '$toDate': datetime.utcnow()
                                        }, {
                                            '$toDate': '$date_of_birth'
                                        }
                                    ]
                                }, 31536000000
                            ]
                        }
                    }, 
                    'else': None
                }
            }
        }
    }]
    if request.args.get("healthcare_staff_id")!=None:
        temp = {
        '$match': {
            'patient_info.healthcare_staff_id': {
                '$elemMatch': {
                    '$in': [
                        ObjectId(request.args.get("healthcare_staff_id"))
                    ]
                }
            }
        }}
        filter.insert(3,temp)
    if request.args.get("gender")!=None:
        temp = {
        '$match': {
            'gender': request.args.get("gender")
        }}
        filter.insert(0,temp)
    if request.args.get("usia")!=None:
        min = 0
        max = 1000
        golongan = request.args.get("usia").lower()
        if golongan == "anak-anak":
            max = 12
        elif golongan == "remaja":
            min=13
            max=22
        elif golongan == "dewasa":
            min = 23
            max = 55
        elif golongan == "manula":
            min = 56
        else:
            raise Exception("Golongan usia tidak valid")
        temp = {
        '$match': {
            'usia': {
                '$gte': min, 
                '$lte': max
            }
        }}
        filter.append(temp)
    data = aggregate_to_collection("user",filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    if len(data)==0:
        raise Exception("Tidak ada pasien yang memenuhi kriteria filter")
    return data

def insert_patient_to_healthcare_staff(reqeust):
    patient = get_from_collection("user", {"_id": ObjectId(reqeust.form["patient_id"])})
    patient = json.loads(bson.json_util.dumps(list(patient)))
    if len(patient) == 0:
        raise Exception(f"pasien dengan id pasien {reqeust.form['patient_id']} tidak ditemukan")
    patient = patient[0]

    healthcare_staff = get_from_collection("user", {"_id": ObjectId(reqeust.form["healthcare_staff_id"])})
    healthcare_staff = json.loads(bson.json_util.dumps(list(healthcare_staff)))
    if len(healthcare_staff) == 0:
        raise Exception(f"perawat dengan id perawat {reqeust.form['healthcare_staff_id']} tidak ditemukan")
    healthcare_staff = healthcare_staff[0]

    patient_info = get_from_collection("patient_info", {"user_id": ObjectId(patient["_id"]["$oid"])})
    patient_info = json.loads(bson.json_util.dumps(list(patient_info)))
    if len(patient_info) == 0:
        raise Exception(f"user dengan id pasien {reqeust.form['patient_id']} bukan pasien")
    patient_info = patient_info[0]

    healthcare_staff_info = get_from_collection("healthcare_staff_info", {"user_id": ObjectId(healthcare_staff["_id"]["$oid"])})
    healthcare_staff_info = json.loads(bson.json_util.dumps(list(healthcare_staff_info)))
    if len(healthcare_staff_info) == 0:
        raise Exception(f"user dengan id perawat {reqeust.form['healthcare_staff_id']} bukan perawat")
    healthcare_staff_info = healthcare_staff_info[0]

    # Convert all healthcare_staff_id in patient_info to ObjectId
    patient_info["healthcare_staff_id"] = [
        ObjectId(item["$oid"]) if isinstance(item, dict) and "$oid" in item else ObjectId(item)
        for item in patient_info["healthcare_staff_id"]
    ]
    # Add new healthcare_staff_id as ObjectId
    patient_info["healthcare_staff_id"].append(ObjectId(reqeust.form["healthcare_staff_id"]))

    # Convert all patient_id in healthcare_staff_info to ObjectId
    healthcare_staff_info["patient_id"] = [
        ObjectId(item["$oid"]) if isinstance(item, dict) and "$oid" in item else ObjectId(item)
        for item in healthcare_staff_info["patient_id"]
    ]
    # Add new patient_id as ObjectId
    healthcare_staff_info["patient_id"].append(ObjectId(reqeust.form["patient_id"]))

    # Update MongoDB collections
    update_from_collection("patient_info", patient_info["_id"]["$oid"], {"healthcare_staff_id": patient_info["healthcare_staff_id"]})
    update_from_collection("healthcare_staff_info", healthcare_staff_info["_id"]["$oid"], {"patient_id": healthcare_staff_info["patient_id"]})

    return "Berhasil menambah pasien ke list perawat"

def get_one_patient(patient_id):
    filter = [
    {
        '$match': {
            '_id': ObjectId(patient_id)
        }
    }, {
        '$lookup': {
            'from': 'patient_info', 
            'localField': '_id', 
            'foreignField': 'user_id', 
            'as': 'patient_info'
        }
    }, {
        '$addFields': {
            'roles': 'pasien'
        }
    },
    {
        '$addFields': {
            'usia': {
                '$cond': {
                    'if': {
                        '$ne': [
                            '$date_of_birth', None
                        ]
                    }, 
                    'then': {
                        '$floor': {
                            '$divide': [
                                {
                                    '$subtract': [
                                        {
                                            '$toDate': datetime.utcnow()
                                        }, {
                                            '$toDate': '$date_of_birth'
                                        }
                                    ]
                                }, 31536000000
                            ]
                        }
                    }, 
                    'else': None
                }
            }
        }
    }]
    data = aggregate_to_collection("user",filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    data = data[0]
    return data

def get_one_healthcare_staff(healthcare_staff_id):
    filter = [
    {
        '$match': {
            '_id': ObjectId(healthcare_staff_id)
        }
    }, {
        '$lookup': {
            'from': 'healthcare_staff_info', 
            'localField': '_id', 
            'foreignField': 'user_id', 
            'as': 'healthcare_staff_info'
        }
    }, {
        '$addFields': {
            'roles': 'perawat'
        }
    },
    {
        '$addFields': {
            'usia': {
                '$cond': {
                    'if': {
                        '$ne': [
                            '$date_of_birth', None
                        ]
                    }, 
                    'then': {
                        '$floor': {
                            '$divide': [
                                {
                                    '$subtract': [
                                        {
                                            '$toDate': datetime.utcnow()
                                        }, {
                                            '$toDate': '$date_of_birth'
                                        }
                                    ]
                                }, 31536000000
                            ]
                        }
                    }, 
                    'else': None
                }
            }
        }
    }]
    data = aggregate_to_collection("user",filter)
    data = json.loads(bson.json_util.dumps(list(data)))
    data = data[0]
    # print("test")
    return data