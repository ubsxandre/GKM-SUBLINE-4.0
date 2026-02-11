from app_center import db
import datetime
class m_cookie_api(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  cookie = db.Column(db.Text)
  created_by = db.Column(db.String(100))
  created_date = db.Column(db.DateTime)
  status_aktif = 1