from flask.helpers import flash
from app_center.api import controller_api
from app_center.backend.master import model_master
from app_center.authentication.akses import controller_akses
from app_center.authentication.login import model
from app_center.modules import controller_module
from flask import render_template, redirect, url_for, request, jsonify, send_file
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func, case, and_, or_, cast, DATE, INT, literal_column, union_all
from datetime import datetime, timedelta
import json, os, pandas as pd, numpy as np
from io import BytesIO
from app_center import db, org, client, org_wit, client_wit

'''' INITIAL MODEL MASTER '''


''' INIT TRANSACTION '''

''' 4.0 '''
def daterange(start_date, end_date):
  for n in range(int((end_date - start_date).days)):
    yield start_date + timedelta(n)

