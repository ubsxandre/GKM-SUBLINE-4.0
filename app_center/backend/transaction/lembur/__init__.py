from flask import Blueprint

be_lembur_init = Blueprint('be_lembur', __name__, static_folder='static', template_folder='templates')

from app_center.backend.transaction.lembur import view_lembur