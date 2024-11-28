import pymongo
from flask import Blueprint, route, method, request
from wound.keperawatan_luka import controller

bp = Blueprint('keperawatan_luka-controller', __name__, url_prefix='/')
