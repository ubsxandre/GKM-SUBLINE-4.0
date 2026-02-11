from flask import Blueprint

be_testing_init = Blueprint('be_testing', __name__, static_folder='static', template_folder='templates')

from app_center.backend.testing import view_testing