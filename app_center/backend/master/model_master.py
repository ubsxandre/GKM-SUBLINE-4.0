from app_center import db
from datetime import datetime
from sqlalchemy import UniqueConstraint

def waktu_sekarang():
  return datetime.now()

class MasterRoles(db.Model):
  """
  Master Roles
  """
  __tablename__ = 'm_roles'
  id = db.Column(db.Integer, primary_key=True)
  role = db.Column(db.String(100))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')

  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}

class MasterRolesHistory(db.Model):
  """
  Master Roles History
  """
  __tablename__ = 'm_roles_history'
  __bind_key__ = 'history'
  id = db.Column(db.Integer, primary_key=True)
  id_history = db.Column(db.Integer)
  role = db.Column(db.String(100))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')

  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}
  
class MasterPages(db.Model):
  """
  Master Pages
  """
  __tablename__ = 'm_pages'
  id = db.Column(db.Integer, primary_key=True)
  page = db.Column(db.String(100))
  crud = db.Column(db.String(1))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')

  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}

class MasterPagesHistory(db.Model):
  """
  Master Pages History
  """
  __tablename__ = 'm_pages_history'
  __bind_key__ = 'history'
  id = db.Column(db.Integer, primary_key=True)
  id_history = db.Column(db.Integer)
  page = db.Column(db.String(100))
  crud = db.Column(db.String(1))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')

  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}
  
class MasterAkses(db.Model):
  """
  Master Akses
  """
  __tablename__ = 'm_akses'
  id = db.Column(db.Integer, primary_key=True)
  id_role = db.Column(db.Integer)
  id_page = db.Column(db.Integer)
  akses = db.Column(db.String(100))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')

  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}
  
class MasterAksesHistory(db.Model):
  """
  Master Akses History
  """
  __tablename__ = 'm_akses_history'
  __bind_key__ = 'history'
  id = db.Column(db.Integer, primary_key=True)
  id_history = db.Column(db.Integer)
  id_role = db.Column(db.Integer)
  id_page = db.Column(db.Integer)
  akses = db.Column(db.String(100))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')

  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}
  
class MasterAksesManagement(db.Model):
  """
  Master Akses Management Akses
  """
  __tablename__ = 'm_akses_management'
  id = db.Column(db.Integer, primary_key=True)
  nik = db.Column(db.String(10))
  id_role = db.Column(db.Integer)
  id_page = db.Column(db.Integer)
  akses = db.Column(db.String(100))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')

  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}
  
class MasterAksesManagementHistory(db.Model):
  """
  Master Akses Management History
  """
  __tablename__ = 'm_akses_management_history'
  __bind_key__ = 'history'
  id = db.Column(db.Integer, primary_key=True)
  id_history = db.Column(db.Integer)
  nik = db.Column(db.String(10))
  id_role = db.Column(db.Integer)
  id_page = db.Column(db.Integer)
  akses = db.Column(db.String(100))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')

  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}

class MasterEmployees(db.Model):
  """
  Master Employees
  """
  __tablename__ = 'm_employees'
  id = db.Column(db.Integer, primary_key=True)
  id_code = db.Column(db.String(100))
  nik = db.Column(db.String(10))
  nama = db.Column(db.String(100))
  bagian = db.Column(db.String(100))
  department = db.Column(db.String(100))
  jabatan = db.Column(db.String(100))
  golongan = db.Column(db.String(2))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')
  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}

class MasterEmployeesHistory(db.Model):
  """
  Master Employees History
  """
  __tablename__ = 'm_employees_history'
  __bind_key__ = "history"
  id = db.Column(db.Integer, primary_key=True)
  id_history = db.Column(db.Integer)
  id_code = db.Column(db.String(100))
  nik = db.Column(db.String(10))
  nama = db.Column(db.String(100))
  bagian = db.Column(db.String(100))
  department = db.Column(db.String(100))
  jabatan = db.Column(db.String(100))
  golongan = db.Column(db.String(2))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')
  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}

class MasterBagian(db.Model):
  """
  Master Bagian
  """
  __tablename__ = "m_bagian"
  id = db.Column(db.Integer, primary_key=True)
  id_bagian_api = db.Column(db.String(10))
  bagian = db.Column(db.String(100))
  keterangan = db.Column(db.String(100))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')
  
  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}

class MasterBagianHistory(db.Model):
  """
  Master Bagian History
  """
  __tablename__ = "m_bagian_history"
  __bind_key__ = "history"
  id = db.Column(db.Integer, primary_key=True)
  id_history = db.Column(db.Integer)
  id_bagian_api = db.Column(db.String(10))
  bagian = db.Column(db.String(100))
  keterangan = db.Column(db.String(100))
  created_by = db.Column(db.String(100), default='SYSTEM')
  created_date = db.Column(db.DateTime, default=waktu_sekarang)
  status_aktif = db.Column(db.String(2), default='1')
  
  def to_dict(self):
    return {row:getattr(self,row) for row in dir(self) if not row.startswith('_') and row not in ['registry', 'query_class', 'query', 'metadata'] and not callable(getattr(self,row))}
