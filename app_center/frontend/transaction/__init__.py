from flask import Blueprint

fe_transaction_init = Blueprint('fe_transaction', __name__, static_folder='static', template_folder='templates')

from app_center.frontend.transaction import view_transaction