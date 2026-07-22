from flask import Blueprint

be_report_in_out_init = Blueprint('be_report_in_out', __name__, static_folder='static', template_folder='templates')

from app_center.backend.report.in_out import view_report_in_out