from flask import Blueprint

be_dashboard_init = Blueprint('be_dashboard', __name__, static_folder='static', template_folder='templates')

from app_center.backend.dashboard import view_dashboard