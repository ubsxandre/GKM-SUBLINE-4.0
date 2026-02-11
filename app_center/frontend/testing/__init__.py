from flask import Blueprint

fe_testing_init = Blueprint('fe_te4sting', __name__, static_folder='static', template_folder='templates')

from app_center.frontend.testing import view_testing