from flask import Blueprint

fe_login_init = Blueprint('fe_login', __name__, static_folder='static', template_folder='templates')

from app_center.frontend.login import view