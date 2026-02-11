from flask import Blueprint

fe_master_init = Blueprint('fe_master', __name__, static_folder='static', template_folder='templates')

from app_center.frontend.master import view_master