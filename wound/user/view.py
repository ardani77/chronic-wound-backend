import pymongo
from flask import Blueprint, request, Response
from wound.model import db_user
import json

bp = Blueprint('user-view', __name__, url_prefix='/')
