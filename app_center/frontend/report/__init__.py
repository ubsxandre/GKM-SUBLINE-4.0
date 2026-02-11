from flask import Blueprint

fe_report_init = Blueprint('fe_report', __name__, static_folder='static', template_folder='templates')

from app_center.frontend.report import view_report