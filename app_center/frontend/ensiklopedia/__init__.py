from flask import Blueprint

fe_ensiklopedia_init = Blueprint('fe_ensiklopedia', __name__, static_folder='static', template_folder='templates')

from app_center.frontend.ensiklopedia import view_ensiklopedia