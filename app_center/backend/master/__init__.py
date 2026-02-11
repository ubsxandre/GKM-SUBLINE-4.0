from flask import Blueprint

be_master_init = Blueprint('be_master', __name__, static_folder='static', template_folder='templates')

from app_center.backend.master import view_master