# coding: utf-8
from flask import Blueprint

project = Blueprint('project', __name__)

from . import views
