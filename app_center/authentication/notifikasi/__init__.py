from flask import Blueprint

app_notifikasi = Blueprint('notifikasi', __name__, static_folder='static', template_folder='templates')

from app_center.authentication.notifikasi import view_notifikasi