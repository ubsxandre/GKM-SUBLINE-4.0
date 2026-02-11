from datetime import datetime
from flask_login import current_user
from app_center import db
from datetime import datetime

def waktu_sekarang():
  return datetime.now()
class PageCounter(db.Model):
  """
  COUNTER ORANG BUKA PAGES
  """  
  __tablename__ = 'page_counter'
  id = db.Column(db.Integer, primary_key=True)
  page = db.Column(db.String(100))
  nik = db.Column(db.String(10))
  id_unix = db.Column(db.String(100), unique=True)
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
