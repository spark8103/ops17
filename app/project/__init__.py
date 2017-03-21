from flask import Blueprint

user = Blueprint('project', __name__)

from . import views
