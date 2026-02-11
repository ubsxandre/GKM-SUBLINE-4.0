from app_center import db
from flask import abort
from flask_login import UserMixin, current_user
from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView 
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

''' MODEL TABEL MASTER USER '''
class User(db.Model, UserMixin ):
  """ Model Tabel Database untuk menyimpan data USER """
  id = db.Column(db.Integer, primary_key=True)
  nik = db.Column(db.String(10), unique=True)
  nama = db.Column(db.String(50))
  password = db.Column(db.String(128))
  departemen = db.Column(db.String(100))
  golongan = db.Column(db.String(100))
  id_role = db.Column(db.Integer)
  created_by = db.Column(db.String(100))
  created_date = db.Column(db.DateTime)
  status_aktif = db.Column(db.String(2), default=1)
  
  def set_password(self, password):
    self.password  = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)
  

  

  
  