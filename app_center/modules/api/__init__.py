from flask import Blueprint

app_api = Blueprint('api', __name__, static_folder='static', template_folder='templates')

from app_center.api import view_api