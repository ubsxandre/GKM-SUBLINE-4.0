from app_center import db
from datetime import datetime
from sqlalchemy import UniqueConstraint

def waktu_sekarang():
  return datetime.now()
