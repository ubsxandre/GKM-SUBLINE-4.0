from flask.helpers import flash
from app_center.backend.master import model_master
from app_center.authentication.login import model
from flask import render_template, redirect, url_for, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app_center import db
from flask_login import login_user, login_required, current_user, logout_user
from app_center.authentication.akses import controller_akses
from app_center.api import controller_api
from sqlalchemy import func, case, and_, or_, cast, DATE, INT, literal_column, union_all, inspect
from sqlalchemy.orm import aliased, Session
from datetime import datetime, timedelta, time
from app_center.modules import controller_module
from app_center.backend.transaction.absensi import model_absensi
import json, os, pandas as pd, numpy as np