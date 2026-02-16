from app_center import db
from datetime import datetime
from sqlalchemy import UniqueConstraint

def waktu_sekarang():
  return datetime.now()


class TransLembur(db.Model):
  """
  Transaksi Lembur
  """
  __tablename__ = 't_lembur'
  id = db.Column(db.Integer, primary_key=True)
  nik = db.Column(db.String(100))
  nama = db.Column(db.String(100))
  start_lembur = db.Column(db.DateTime)
  end_lembur = db.Column(db.DateTime)
  lokasi = db.Column(db.String(100))
  keterangan = db.Column(db.String(250))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')

  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}

class TransLemburHistory(db.Model):
  """
  Transaksi Lembur History
  """
  __tablename__ = 't_lembur_history'
  __bind_key__ = 'history'
  id = db.Column(db.Integer, primary_key=True)
  id_history = db.Column(db.Integer)
  nik = db.Column(db.String(100))
  nama = db.Column(db.String(100))
  start_lembur = db.Column(db.DateTime)
  end_lembur = db.Column(db.DateTime)
  lokasi = db.Column(db.String(100))
  keterangan = db.Column(db.String(250))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')

  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}
  