from flask import Blueprint

app_akses = Blueprint('akses', __name__, static_folder='static', template_folder='templates')

from app_center.authentication.akses import view_akses