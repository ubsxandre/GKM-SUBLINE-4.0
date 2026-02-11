from flask import Blueprint

be_ensiklopedia_init = Blueprint('be_ensiklopedia', __name__, static_folder='static', template_folder='templates')

from app_center.backend.ensiklopedia import view_ensiklopedia