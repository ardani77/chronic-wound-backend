import pymongo
from flask import Blueprint, request, Response
from wound.model import db_data_perawat
import json

bp = Blueprint('perawat-view', __name__, url_prefix='/')