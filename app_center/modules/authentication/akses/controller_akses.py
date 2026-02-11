from app_center.authentication.akses import model_akses as ma
from app_center import db, ERRORLOGDIR, SAVED_AUTH_TOKEN, SAVED_HASHED_NIK, reddb
from app_center.errors import handlers
from functools import wraps
from app_center.modules import controller_module
from flask_login import current_user
from flask import render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
import os, socket
from sqlalchemy import func, case, and_, or_, cast, DATE, INT, literal_column, union_all



def page_counter(page):
  def theCounter(f):
    @wraps(f)
    def theProcessCounter(*args, **kwargs):
      if current_user.is_authenticated:
        date_now = datetime.now().strftime('%d-%m-%Y')
        nik = current_user.nik
        id_unix = f"{nik}-{date_now}-{page}"
        cek_count = db.session.query(ma.PageCounter.id).filter(ma.PageCounter.id_unix==id_unix).count()
        if cek_count == 0:
          try:
            add = ma.PageCounter(
              page = page,
              id_unix = id_unix,
              nik = nik
            )          
            db.session.add(add)
            db.session.commit()
          except:
            pass
      return f(*args, **kwargs)
    return theProcessCounter
  return theCounter

def autentikasi(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    date_now = datetime.now().strftime('%d-%m-%Y')
    if current_user.is_authenticated:
      get_bearer = current_user.bearer_token
      if get_bearer != None and get_bearer.startswith('Bearer') == True:
        bearer = get_bearer.split('Bearer ')[-1]
        bearer_app = None
        if os.environ.get('FLASK_RUN_HOST') == '172.20.140.98':
          bearer_app = reddb.get(f"{current_user.nik}-{date_now}") 
        else:
          if f"{current_user.nik}-{date_now}" in SAVED_AUTH_TOKEN:
            bearer_app = SAVED_AUTH_TOKEN[f"{current_user.nik}-{date_now}"]
        if bearer == bearer_app:
          return f(*args, **kwargs)
        else:
          current_user.bearer_token = controller_module.generateBearerToken(current_user.nik)
          return f(*args, **kwargs)
      else:
        current_user.bearer_token = controller_module.generateBearerToken(current_user.nik)
        return f(*args, **kwargs)
    else:
      get_bearer = request.headers.get('Authorization')
      if get_bearer != None and get_bearer.startswith('Bearer') == True:
        bearer = get_bearer.split('Bearer ')[-1]
        nik = controller_module.convertBearerTokenToNik(bearer) 
        bearer_app = None
        if os.environ.get('FLASK_RUN_HOST') == '172.20.140.98':
          bearer_app = reddb.get(f"{nik}-{date_now}") 
        else:
          if f"{nik}-{date_now}" in SAVED_AUTH_TOKEN:
            bearer_app = SAVED_AUTH_TOKEN[f"{nik}-{date_now}"]
        if bearer == bearer_app:
          return f(*args, **kwargs)
        else:
          return jsonify({"status":"error", 'message':'Bearer Token Salah'})
      else:
        return jsonify({"status":"error", "message": "Not authorized to access this resource"}), 401
  return wrapper
    
def getNikBearer():    
  if current_user.is_authenticated == True:
    get_bearer = current_user.bearer_token
  else:
    get_bearer = request.headers.get('Authorization')
  bearer = get_bearer.split('Bearer ')[-1]
  return SAVED_HASHED_NIK[bearer]
  
def login_user(nik):
  """ Untuk meloginkan user via API
  
  Khusus ini importnya ditaruh didalam function agar tidak mengganggu auto documentation
  """
  from app_center.backend.master import model_master
  from app_center.authentication.login import model
  USER = model.User
  MROLES = model_master.MasterRoles
  MAKMA = model_master.MasterAksesManagement
  MPAGES = model_master.MasterPages
  user = USER.query.filter_by(nik=nik, status_aktif=1).first()
  data_user = user.__dict__   
  data_user['env'] = os.environ.get('FLASK_ENV')
  therole = db.session.query(MROLES.role).filter_by(id=data_user['id_role']).first()
  theakses = db.session.query(USER).with_entities(MAKMA.id, USER.nik, MAKMA.id_role, MROLES.role, 
                                                  MAKMA.id_page, MPAGES.page, MAKMA.akses, 
                                                  )\
                                                .outerjoin(MAKMA, and_(MAKMA.nik==USER.nik, MAKMA.id_role==USER.id_role, MAKMA.status_aktif==1))\
                                                .join(MROLES, and_(MROLES.id==MAKMA.id_role, MROLES.status_aktif==1))\
                                                .join(MPAGES, and_(MPAGES.id==MAKMA.id_page, MPAGES.status_aktif==1))\
                                                .filter(USER.status_aktif==1,USER.nik==data_user['nik']).all()
  list_akses = []
  list_page = []
  if theakses:
    for ta in theakses:
      tdict = ta._asdict()
      if tdict['page'] not in list_page:
        list_page.append(tdict['page'])
      list_akses.append(f"{tdict['page']}-{tdict['akses']}")
  data_user['list_akses'] = list_akses
  data_user['list_page'] = list_page
  data_user['nama_roles'] = therole.role if therole else None
  return data_user
  
def cek_page(page):
  def cekPage(f):
    @wraps(f)
    def processPage(*args, **kwargs):
      if current_user.is_authenticated:
        if current_user.nama_roles == 'DEVELOPER':
          return f(*args, **kwargs)
        elif page in current_user.list_page:
          return f(*args, **kwargs)
        else:
          return handlers.unauthorized_error("")
      else:
        get_bearer = request.headers.get('Authorization')
        if get_bearer != None and get_bearer.startswith('Bearer') == True:
          bearer = get_bearer.split('Bearer ')[-1]
          nik = controller_module.convertBearerTokenToNik(bearer)
          user = login_user(nik)
          if user['nama_roles'] == 'DEVELOPER':
            return f(*args, **kwargs)
          elif page in current_user.list_page:
            return f(*args, **kwargs)
          return handlers.unauthorized_error("")
        return handlers.unauthorized_error("")
    return processPage
  return cekPage  
  
def cek_akses_api(akses):
  def cekAksesApi(f):
    @wraps(f)
    def processAksesApi(*args, **kwargs):
      if current_user.is_authenticated:
        if current_user.nama_roles == 'DEVELOPER':
          return f(*args, **kwargs)
        elif akses in current_user.list_akses:
          return f(*args, **kwargs)
        else:
          return jsonify({"status":"error", "message": "You don't have permission to access this API"}), 401
      else:
        get_bearer = request.headers.get('Authorization')
        if get_bearer != None and get_bearer.startswith('Bearer') == True:
          bearer = get_bearer.split('Bearer ')[-1]
          nik = controller_module.convertBearerTokenToNik(bearer)
          user = login_user(nik)
          if user['nama_roles'] == 'DEVELOPER':
            return f(*args, **kwargs)
          elif akses in current_user.list_akses:
            return f(*args, **kwargs)
          else:
            return jsonify({"status":"error", "message": "You don't have permission to access this API"}), 401
        else:
          return jsonify({"status":"error", "message": "Not authorized to access this resource"}), 401
    return processAksesApi
  return cekAksesApi

def getSession():
  try:
    qcounter = db.session.query(ma.PageCounter).with_entities(ma.PageCounter.nik, func.date_format(ma.PageCounter.created_date, '%Y-%m-%d'))\
                                              .group_by(ma.PageCounter.nik,
                                                  func.date_format(ma.PageCounter.created_date, '%Y-%m-%d')).count()
    data = qcounter
    return jsonify({'status':'success', 'message':'Counter retrieved successfully', 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})