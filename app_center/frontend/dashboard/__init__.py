from flask import Blueprint

fe_dashboard_init = Blueprint('fe_dashboard', __name__, static_folder='static', template_folder='templates')

from app_center.frontend.dashboard import view_dashboard