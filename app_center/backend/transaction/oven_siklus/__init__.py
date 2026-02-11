from flask import Blueprint

be_oven_siklus_init = Blueprint('be_oven_siklus', __name__, static_folder='static', template_folder='templates')

from app_center.backend.transaction.oven_siklus import view_oven_siklus