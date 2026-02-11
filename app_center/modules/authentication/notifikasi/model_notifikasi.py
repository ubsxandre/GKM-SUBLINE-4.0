from app_center import db

# class cache_notifikasi_andon(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   nomor_mesin = db.Column(db.String(10))
#   status = db.Column(db.String(20))
  
# class m_notifikasi(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   nik = db.Column(db.String(10))
#   message = db.Column(db.Text)
#   status_dibaca = db.Column(db.String(2), default=0) 
#   tanggal_baca = db.Column(db.DateTime)
#   created_date = db.Column(db.DateTime)
#   status_aktif = db.Column(db.String(2), default=1)
#   route = db.Column(db.String(300))
#   kategori = db.Column(db.String(99))
#   title = db.Column(db.String(99))
#   status_andon = db.Column(db.String(20))

#   def __repr__(self):
#     return f"<m_notifikasi {self.id} {self.nik}>" 
#   def get_id(self):
#     return (self.id)