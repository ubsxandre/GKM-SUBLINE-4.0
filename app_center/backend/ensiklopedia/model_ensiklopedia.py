from app_center import db
from datetime import datetime

def waktu_sekarang():
  waktu = datetime.now()
  return waktu

class Ensiklopedia(db.Model):
  __tablename__ = 'ensiklopedia'
  id = db.Column(db.Integer, primary_key=True)
  judul = db.Column(db.String(99))
  file_name = db.Column(db.String(255))
  ekstension = db.Column(db.String(20))
  ukuran_file = db.Column(db.String(20))
  tipe = db.Column(db.String(10), default='file')
  keterangan = db.Column(db.String(100))
  created_by = db.Column(db.String(20))
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default=1)
  
  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}

class EnsiklopediaHistory(db.Model):
  __tablename__ = 'ensiklopedia_history'
  __bind_key__ = 'history'
  id = db.Column(db.Integer, primary_key=True)
  id_history = db.Column(db.Integer)
  judul = db.Column(db.String(99))
  file_name = db.Column(db.String(255))
  ekstension = db.Column(db.String(20))
  ukuran_file = db.Column(db.String(20))
  tipe = db.Column(db.String(10), default='file')
  keterangan = db.Column(db.String(100))
  created_by = db.Column(db.String(20))
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default=1)

  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}