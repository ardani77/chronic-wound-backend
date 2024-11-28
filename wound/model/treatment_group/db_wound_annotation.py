import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId
from wound.model.db_setting import *
from werkzeug.utils import secure_filename
import time
import os
import numpy
from wound import utils
import ast
def create_annotation(path,request):
    data = {}
    nullable = {"manual_annotation": "vector_list", "minor_axis": "vector_list", "major_axis": "vector_list","circle_center":"vector","radius": "float"}
    for param in nullable.keys():
        if request.form.get(param)!='""' and request.form.get(param)!="" and request.form.get(param)!="''" and request.form.get(param)!=None:
            print(param,request.form.get(param))
            if nullable[param]== "float":
                data[param] = float(request.form[param])
            elif nullable[param] == "vector_list" or nullable[param] == "vector":
                data[param] = ast.literal_eval(request.form[param])
    check = ["circle_center","radius"]
    gate=True
    for param in check:
        if request.form.get(param)!='""' and request.form.get(param)!="" and request.form.get(param)!="''" and request.form.get(param)!=None:
            continue
        gate=False
    if gate:
        data["automatic_annotation"] = utils.automatic_annotation(path,data["circle_center"][0],data["circle_center"][1],data["radius"])
    return insert_to_collection("wound_annotation",data)