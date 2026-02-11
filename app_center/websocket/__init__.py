from flask import Blueprint

app_socket = Blueprint('websocket', __name__, static_folder='static', template_folder='templates')

from app_center.websocket import view_websocket