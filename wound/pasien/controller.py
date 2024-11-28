import pymongo
from flask import Blueprint, request, Response
from wound.model import db_data_pasien
import json

bp = Blueprint('pasien-controller', __name__, url_prefix='/')
