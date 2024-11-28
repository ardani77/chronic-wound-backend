import pymongo
from flask import Blueprint, request, Response
from wound.model import db_data_pasien, db_data_perawat
import json

bp = Blueprint('auth-view', __name__, url_prefix='/')