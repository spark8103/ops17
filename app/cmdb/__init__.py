# coding: utf-8
from flask import Blueprint

cmdb = Blueprint('cmdb', __name__)

from . import views
