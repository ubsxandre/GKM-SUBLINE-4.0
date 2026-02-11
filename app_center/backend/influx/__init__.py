from flask import Blueprint

be_influx_init = Blueprint('be_influx', __name__, static_folder='static', template_folder='templates')

from app_center.backend.influx import view_influx