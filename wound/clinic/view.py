import pymongo
from flask import Blueprint, route, method, request
from wound.clinic import controller

bp = Blueprint('clinic-controller', __name__, url_prefix='/')
