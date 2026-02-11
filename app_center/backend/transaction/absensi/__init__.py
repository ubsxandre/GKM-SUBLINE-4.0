from flask import Blueprint

be_absensi_init = Blueprint('be_absensi', __name__, static_folder='static', template_folder='templates')

from app_center.backend.transaction.absensi import view_absensi