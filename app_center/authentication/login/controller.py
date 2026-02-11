from flask.helpers import flash
from app_center.authentication.login import app_login_init, controller, model
from flask import render_template, redirect, url_for, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app_center import db, AUTH_KEY
from flask_login import login_user, login_required, current_user, logout_user
from flask_minify import Minify, decorators as minify_decorators
from app_center.api import controller_api
from sqlalchemy import func, and_, or_, cast, DATE, INT
from datetime import datetime, timedelta
from app_center.modules import controller_module
from app_center.backend.master import model_master


'''' INITIAL MODEL '''
USER = model.User
MROLES = model_master.MasterRoles
# MROLES = model.m_roles
# MROLESHIST = model.m_roles_history
# MPAGE = model.m_page
# MAKSES = model.m_akses
# MAKSESHIST = model.m_akses_history

def loginPost():
  try:
    nik = request.form.get('nik')
    password = request.form.get('password')
    remember = True if request.form.get('rememberme') else False
    user_dev = USER.query.filter(USER.nik==nik, USER.password==password, 
                                USER.password!='SSO', USER.status_aktif==1).first()
    if user_dev:
      get_roles = db.session.query(MROLES.role).filter(MROLES.id==user_dev.id_role).first()
      if get_roles and get_roles.role=='DEVELOPER':
        if remember == True:
          login_user(user_dev, remember=remember, duration=timedelta(days=7))
        else:
          login_user(user_dev)
        return jsonify({'status':'success', 'message': 'Login successful'})
    sso = controller_api.getSSO(nik, password)
    if sso == 'T':
      # return jsonify({'status':'warning', 'message': 'Password SSO Salah!'})
      flash('Password SSO Salah!', 'warning')
      return True
    elif sso == 'X':
      # return jsonify({'status':'warning', 'message': 'Password SSO Kadaluarsa, Harap Ganti Password SSO Anda!'})
      flash('Password SSO Kadaluarsa, Harap Ganti Password SSO Anda!', 'warning')
      return True
    elif sso == 'Z':
      # return jsonify({'status':'warning', 'message': 'NIK Tidak Terdaftar Kedalam SSO!'})
      flash('NIK Tidak Terdaftar Kedalam SSO!', 'warning')
      return True
    elif sso == 'XZ':
      # return jsonify({'status':'warning', 'message': 'Tidak dapat tersambung kedalam SSO, Harap Periksa Koneksi Anda!'})
      flash('Tidak dapat tersambung kedalam SSO, Harap Periksa Koneksi Anda!', 'warning')
      return True
    else:
      user = USER.query.filter_by(nik=nik, status_aktif=1).first()
      if not user:
        data = controller_api.getAdmkar(nik)
        insert_user = {
                        'nik':nik,
                        'password':'SSO',
                        'nama':data['EmployeeName'],
                        'departemen':data['DepartmentName'],
                        'id_role': None,
                        'golongan': data['Grade'],
                        'created_by': 'SSO',
                        'created_date': datetime.now(),
                        'status_aktif': '1',
                      }
        db.session.add(USER(**insert_user))
        db.session.commit()
      user = USER.query.filter_by(nik=nik, status_aktif=1).first()
      if remember == True:
        login_user(user, remember=remember, duration=timedelta(days=7))
      else:
        login_user(user)
      token =  controller_module.generateBearerToken(user.nik).replace("Bearer ", "")
      # flash("Berhasil Login!", 'success')
      return False
      # return jsonify({'status':'success', 'message': 'Login successful', 'token':token})
  except Exception as e:
    print(e) 
    return jsonify({'status':'error', 'message':str(e)})
  finally:
    db.session.close()

''' SUBMIT LOGIN '''
def login():
  """ Fungsi untuk memproses session saat login.
      Username dan password akan dicek terlebih dahulu sebelum masuk ke aplikasi. """
  try:
    data = request.get_json()
    nik = data.get('nik')
    password = data.get('password')
    authkey = data.get('authKey')
    remember = True if data.get('rememberme') else False
    user_dev = USER.query.filter(USER.nik==nik, USER.password==password, 
                                USER.password!='SSO', USER.status_aktif==1).first()
    if authkey:
      if authkey == AUTH_KEY:
        berapiapi = USER.query.filter(USER.nik=='ICT',).first()
        token =  controller_module.generateBearerToken(berapiapi.nik).replace("Bearer ", "")
        return jsonify({'status':'success', 'message': 'Login successful', 'token':token},)
      else:
        return jsonify({'status':'warning', 'message': 'Token tidak sesuai!'})
    if user_dev:
      get_roles = db.session.query(MROLES.role).filter(MROLES.id==user_dev.id_role).first()
      if get_roles and get_roles.role=='DEVELOPER':
        if remember == True:
          login_user(user_dev, remember=remember, duration=timedelta(days=7))
        else:
          login_user(user_dev)
        return jsonify({'status':'success', 'message': 'Login successful'})
    sso = controller_api.getSSO(nik, password)
    if sso == 'T':
      return jsonify({'status':'warning', 'message': 'Password SSO Salah!'})
    elif sso == 'X':
      return jsonify({'status':'warning', 'message': 'Password SSO Kadaluarsa, Harap Ganti Password SSO Anda!'})
    elif sso == 'Z':
      return jsonify({'status':'warning', 'message': 'NIK Tidak Terdaftar Kedalam SSO!'})
    elif sso == 'XZ':
      return jsonify({'status':'warning', 'message': 'Tidak dapat tersambung kedalam SSO, Harap Periksa Koneksi Anda!'})
    else:
      user = USER.query.filter_by(nik=nik, status_aktif=1).first()
      if not user:
        data = controller_api.getAdmkar(nik)
        insert_user = {'nik':nik,
                       'password':'SSO',
                       'nama':data['EmployeeName'],
                       'departemen':data['DepartmentName'],
                       'id_role': None,
                       'golongan': data['Grade'],
                       'created_by': 'SSO',
                       'created_date': datetime.now(),
                       'status_aktif': '1',
                       }
        db.session.add(USER(**insert_user))
        db.session.commit()
      user = USER.query.filter_by(nik=nik, status_aktif=1).first()
      if remember == True:
        login_user(user, remember=remember, duration=timedelta(days=7))
      else:
        login_user(user)
      token =  controller_module.generateBearerToken(user.nik).replace("Bearer ", "")

      return jsonify({'status':'success', 'message': 'Login successful', 'token':token})
  except Exception as e:
    print(e) 
    return jsonify({'status':'error', 'message':str(e)})
  finally:
    db.session.close()
    
  

def logout():
    logout_user()  # Clear the session and log out the user
    return jsonify({'status':'success', "message": "Successfully logged out"})


def registrasi():
  """ Fungsi untuk Registrasi user.
      Username dan password akan dicek terlebih dahulu sebelum masuk ke aplikasi. """
  try:
    data = request.get_json()

    nik = data.get('nik')
    nama = data.get('nama')
    password = data.get('password')

    if not nik or not nama or not password:
      print('not nik')
      return jsonify({'status':'warning', 'message': 'All fields are required'})

    if USER.query.filter_by(nik=nik, status_aktif=1).first() is not None:
      print('exists')
      return jsonify({'status':'warning', 'message': 'Username already exists'})

    user = USER(nik=nik, nama=nama)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'status':'success', 'message': 'Registration successful'})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})
  


# ''' ROLES '''
# def get_roles():
#   try:
#     q = db.session.query(MROLES)\
#               .with_entities(MROLES.id, MROLES.roles)\
#               .filter(MROLES.status_aktif==1).all()    
#     data = []
#     for row in q:
#       data.append({
#         'id' : row.id,
#         'roles' : row.roles,
#       })
#     return jsonify({'status':'success', 'message':'ok', 'data':data})
#   except Exception as e:
#     print(e)
#     return jsonify({'status':'error', 'message':str(e)})
  

# ''' GET ROLES BY ID -- PARAM'''
# def get_roles_id():
#   try:
#     filter = []
#     if request.args.get('id') != '':
#       filter.append(MROLES.id==request.args.get('id'),)    
#     q = db.session.query(MROLES)\
#               .with_entities(MROLES.id, MROLES.roles)\
#               .filter(MROLES.status_aktif==1,
#                       *filter,).all()    
#     data = []
#     for row in q:
#       data.append({
#         'id' : row.id,
#         'roles' : row.roles,
#       })
#     return jsonify({'status':'success', 'message':'ok', 'data':data})
#   except Exception as e:
#     print(e)
#     return jsonify({'status':'error', 'message':str(e)})


# ''' ADD ROLES BY ID -- FORM-DATA'''
# def add_roles():
#   try:
#     roles = request.form.get('roles')
#     filter = []
#     if request.form.get('roles') == None:
#       return jsonify({'status':'warning', 'message':'Nama Roles tidak bisa kosong !!!', 'data':[]})
#     filter.append(MROLES.roles==roles)
#     q = db.session.query(MROLES)\
#               .with_entities(MROLES.id, MROLES.roles)\
#               .filter(MROLES.status_aktif==1,
#                       *filter,)
#     q.all()
#     cek = q.first()
#     if cek:
#       return jsonify({'status':'warning', 'message':'Nama Roles sudah digunakan !!!', 'data':[]})
#     data_insert = ({
#       'roles':roles,
#       'created_by':'API', 
#       'created_date':datetime.now(),
#       'status_aktif':1,
#     })
#     print(data_insert)
#     db.session.add(MROLES(**data_insert))
#     db.session.commit()
#     db.session.close()
#     return jsonify({'status':'success', 'message':'Berhasil menambahkan data Master Roles', 'data':data_insert})
#   except Exception as e:
#     print(e)
#     return jsonify({'status':'error', 'message':str(e)})
  

# ''' DELETE ROLES BY ID '''
# def delete_roles_id():
#   try:
#     id = request.args.get('id')
#     filter = []
#     if id == '' or id == None:
#       return jsonify({'status':'success', 'message':'ID Tidak boleh kosong !!!', 'data':[]})
#     filter.append(MROLES.id==id,)       
#     q = db.session.query(MROLES)\
#               .with_entities(MROLES.id, MROLES.roles, MROLES.created_by, MROLES.created_date, MROLES.status_aktif,)\
#               .filter(MROLES.status_aktif==1,
#                       *filter,)    
#     oll = q.all()
#     data = []
#     for row in oll:
#       data.append({
#         'id' : row.id,
#         'roles' : row.roles,
#       })      
#     cek = q.first()
#     ##### Proteksi tidak menemukan ID #####
#     if not cek:
#       return jsonify({'status':'warning', 'message':'ID tidak ditemukan !', 'data':[]})     
#     ##### Insert ke History #####
#     insert_history = ({
#       'id_history': cek.id,
#       'roles': cek.roles,
#       'created_by': cek.created_by,
#       'created_date': cek.created_date,
#       'status_aktif': 1,
#     })
#     db.session.add(MROLESHIST(**insert_history))
#     db.session.commit()
#     ##### Delete data di tabel Main #####
#     data_edit = {'created_by': 'API', #current_user.nik,
#                'created_date':datetime.now(),
#                'status_aktif':0}
#     db.session.query(MROLES).filter(MROLES.id==id).delete()
#     db.session.commit()
#     ##### Menampilkan data yang di delete #####
#     db.session.close()
#     return jsonify({'status':'success', 'message':'Berhasil delete data Roles.', 'data':data})
#   except Exception as e:
#     print(e)
#     return jsonify({'status':'error', 'message':str(e)})


# ''' UPDATE ROLES BY ID '''
# def update_roles_id():
#   try:
#     id = request.form.get('id')
#     roles = request.form.get('roles')
#     filter = []
#     if id == '' or id == None:
#       return jsonify({'status':'success', 'message':'ID Tidak boleh kosong !!!', 'data':[]})
#     filter.append(MROLES.id==id,)  
#     q = db.session.query(MROLES)\
#               .with_entities(MROLES.id, MROLES.roles, MROLES.created_by, MROLES.created_date, MROLES.status_aktif,)\
#               .filter(MROLES.status_aktif==1,
#                       *filter,)
#     cek = q.first()
#     ##### Proteksi tidak menemukan ID #####
#     if not cek:
#       return jsonify({'status':'warning', 'message':'ID tidak ditemukan !', 'data':[]})     
#     ##### Insert ke History #####
#     insert_history = ({
#       'id_history': cek.id,
#       'roles': cek.roles,
#       'created_by': cek.created_by,
#       'created_date': cek.created_date,
#       'status_aktif': cek.status_aktif,
#     })
#     db.session.add(MROLESHIST(**insert_history))
#     db.session.commit()
#     ##### Update data di tabel Main #####
#     data_edit = {
#                'roles': roles,
#                'created_by': 'API', #current_user.nik,
#                'created_date':datetime.now(),
#                'status_aktif':1}
#     db.session.query(MROLES).filter(MROLES.id==id).update(data_edit)
#     db.session.commit()
#     ##### Menampilkan data yang di delete #####
#     db.session.close()
#     return jsonify({'status':'success', 'message':'Haiii', 'data':data_edit})
#   except Exception as e:
#     print(e)
#     return jsonify({'status':'error', 'message':str(e)})
  


def getAksesDatatable():
  datatable = controller_module.Datatable(request.form)

  sort_col_name = ['nik', 'departemen', 'roles', 'golongan', 'status_aktif']
  sort_obj = {
    'nik': USER.nik,
    'departemen': USER.departemen,
    'roles': USER.id_role, 
    'golongan': USER.golongan,
    'status_aktif': USER.status_aktif,
  }

  order = datatable.get_order(sort_col_name=sort_col_name, sort_obj=sort_obj)
  order.append(USER.id)

  jumlah_data_full = db.session.query(USER).filter(USER.status_aktif=='1').count()

  query_filtered = db.session.query(USER).with_entities(USER.nik,
                                                        USER.nama,
                                                        USER.departemen,
                                                        USER.id_role,
                                                        USER.golongan,
                                                        USER.status_aktif,)\
                                          .order_by(*order)
  data_json = datatable.get_data_json_with_entities(query_filtered)
  response = datatable.get_response(jumlah_data_full=jumlah_data_full, data_json=data_json)
  return jsonify(response)


# ''' MASTER AKSES '''
# def get_akses():
#   try:
#     q = db.session.query(MAKSES)\
#               .with_entities(MAKSES.id, 
#                              MAKSES.id_roles, MROLES.roles,
#                              MAKSES.id_page, MPAGE.page,
#                              MAKSES.c, MAKSES.r, MAKSES.u, MAKSES.d,
#                              MAKSES.created_by, MAKSES.created_date, MAKSES.status_aktif,)\
#               .join(MROLES, and_(MROLES.id==MAKSES.id_roles, MAKSES.status_aktif==1))\
#               .join(MPAGE, and_(MPAGE.id==MAKSES.id_page, MPAGE.status_aktif==1))\
#               .filter(MAKSES.status_aktif==1).all()    
#     data = []
#     for row in q:
#       data.append({
#         'id' : row.id,
#         'id_roles': row.id_roles,
#         'roles' : row.roles,
#         'id_page': row.id_page,
#         'page': row.page,
#         'c': row.c, 
#         'r': row.r,
#         'u': row.u,
#         'd': row.d,
#         'created_by': row.created_by, 'created_date': row.created_date, 'status_aktif': row.status_aktif,
#       })
#     return jsonify({'status':'success', 'message':'Data all Master Akses', 'data':data})
#   except Exception as e:
#     print(e)
#     return jsonify({'status':'error', 'message':str(e)})


# ''' GET AKSES BY ID '''
# def get_akses_id():
#   try:
#     filter = []
#     if request.args.get('id') != '':
#       filter.append(MAKSES.id==request.args.get('id'),)    
#     if request.args.get('id_roles') != '':
#       filter.append(MAKSES.id_roles==request.args.get('id_roles'),)   
#     if request.args.get('id') == None or request.args.get('id_roles') == None:
#       return jsonify({'status':'warning', 'message':'Minimal isi 1 Parameter!', 'data':[]})
#     q = db.session.query(MAKSES)\
#               .with_entities(MAKSES.id, 
#                              MAKSES.id_roles, MROLES.roles,
#                              MAKSES.id_page, MPAGE.page,
#                              MAKSES.c, MAKSES.r, MAKSES.u, MAKSES.d,
#                              MAKSES.created_by, MAKSES.created_date, MAKSES.status_aktif,)\
#               .join(MROLES, and_(MROLES.id==MAKSES.id_roles, MAKSES.status_aktif==1))\
#               .join(MPAGE, and_(MPAGE.id==MAKSES.id_page, MPAGE.status_aktif==1))\
#               .filter(MAKSES.status_aktif==1,
#                       *filter,).all()    
#     data = []
#     for row in q:
#       data.append({
#         'id' : row.id,
#         'id_roles': row.id_roles,
#         'roles' : row.roles,
#         'id_page': row.id_page,
#         'page': row.page,
#         'c': row.c, 
#         'r': row.r,
#         'u': row.u,
#         'd': row.d,
#         'created_by': row.created_by, 'created_date': row.created_date, 'status_aktif': row.status_aktif,
#       })
#     return jsonify({'status':'success', 'message':'ok', 'data':data})
#   except Exception as e:
#     print(e)
#     return jsonify({'status':'error', 'message':str(e)})
  

# ''' ADD AKSES -- FORM-DATA'''
# def add_akses():
#   try:
#     name_input_form = request.form.keys()
#     data_insert = {'created_by':'API', 'created_date':datetime.now(), 'status_aktif':1}
#     skip_input = ['']
#     for row in name_input_form:
#       if row not in skip_input:
#         data_insert[row] = request.form.get(row)
#     q = db.session.query(MAKSES)\
#           .with_entities(MAKSES.id, MAKSES.id_roles, MAKSES.id_page,
#                          MAKSES.c, MAKSES.r, MAKSES.u, MAKSES.d,
#                          MAKSES.created_by, MAKSES.created_date, MAKSES.status_aktif)\
#           .filter(MAKSES.status_aktif==1, 
#                   MAKSES.id_roles==data_insert['id_roles'],
#                   MAKSES.id_page==data_insert['id_page'])
#     all = q.all()
#     cek = q.first()
#     if cek:
#       return jsonify({'status':'warning', 'message':'Sudah pernah dibuat !!!'})
#     db.session.add(MAKSES(**data_insert))
#     db.session.commit()
#     ##### Menampilkan data yang di delete #####
#     db.session.close()    
#     return jsonify({'status':'success', 'message':'Berhasil menambahkan data Master Roles', 'data':data_insert})
#   except Exception as e:
#     print(e)
#     return jsonify({'status':'error', 'message':str(e)})
  


# ''' DELETE AKSES BY ID '''
# def delete_akses_id():
#   try:
#     id = request.args.get('id')
#     filter = []
#     if id == None:
#       return jsonify({'status':'success', 'message':'ID Tidak boleh kosong !!!', 'data':[]})
#     filter.append(MAKSES.id==id,)   
#     q = db.session.query(MAKSES)\
#               .with_entities(MAKSES.id, 
#                              MAKSES.id_roles, MROLES.roles,
#                              MAKSES.id_page, MPAGE.page,
#                              MAKSES.c, MAKSES.r, MAKSES.u, MAKSES.d,
#                              MAKSES.created_by, MAKSES.created_date, MAKSES.status_aktif,)\
#               .join(MROLES, and_(MROLES.id==MAKSES.id_roles, MAKSES.status_aktif==1))\
#               .join(MPAGE, and_(MPAGE.id==MAKSES.id_page, MPAGE.status_aktif==1))\
#               .filter(MAKSES.status_aktif==1,
#                       *filter,)
#     oll = q.all()
#     data = []
#     for row in oll:
#       data.append({
#         'id' : row.id,
#         'id_roles': row.id_roles,
#         'id_page': row.id_page,
#         'c': row.c, 
#         'r': row.r,
#         'u': row.u,
#         'd': row.d,
#         'created_by': row.created_by, 'created_date': row.created_date, 'status_aktif': row.status_aktif,
#       })      
#     cek = q.first()
#     print(cek)
#     ##### Proteksi tidak menemukan ID #####
#     if not cek:
#       return jsonify({'status':'warning', 'message':'ID tidak ditemukan !', 'data':[]})     
#     ##### Insert ke History #####
#     insert_history = ({
#       'id_history' : cek.id,
#       'id_roles': cek.id_roles,
#       'id_page': cek.id_page,
#       'c': cek.c, 
#       'r': cek.r,
#       'u': cek.u,
#       'd': cek.d,
#       'created_by': cek.created_by, 'created_date': cek.created_date, 'status_aktif': cek.status_aktif,
#     })
#     db.session.add(MAKSESHIST(**insert_history))
#     db.session.commit()
#     ##### Delete data di tabel Main #####
#     db.session.query(MAKSES).filter(MAKSES.id==id).delete()
#     db.session.commit()
#     ##### Menampilkan data yang di delete #####
#     db.session.close()
#     return jsonify({'status':'success', 'message':'Berhasil delete data Master Akses.', 'data':data})
#   except Exception as e:
#     print(e)
#     return jsonify({'status':'error', 'message':str(e)})


# ''' UPDATE AKSES BY ID '''
# def update_akses_id():
#   try:
#     id = request.form.get('id')
#     id_roles = request.form.get('id_roles')
#     id_page = request.form.get('id_page')
#     filter = []
#     if id == '' or id == None:
#       return jsonify({'status':'success', 'message':'ID Tidak boleh kosong !!!', 'data':[]})
#     filter.append(MAKSES.id==id,)   

#     q = db.session.query(MAKSES)\
#               .with_entities(MAKSES.id, 
#                              MAKSES.id_roles, MROLES.roles,
#                              MAKSES.id_page, MPAGE.page,
#                              MAKSES.c, MAKSES.r, MAKSES.u, MAKSES.d,
#                              MAKSES.created_by, MAKSES.created_date, MAKSES.status_aktif,)\
#               .join(MROLES, and_(MROLES.id==MAKSES.id_roles, MAKSES.status_aktif==1))\
#               .join(MPAGE, and_(MPAGE.id==MAKSES.id_page, MPAGE.status_aktif==1))\
#               .filter(MAKSES.status_aktif==1,
#                       *filter,)
#     cek = q.first()
#     ##### Proteksi tidak menemukan ID #####
#     if not cek:
#       return jsonify({'status':'warning', 'message':'ID tidak ditemukan !', 'data':[]})     
#     ##### Insert ke History #####
#     insert_history = ({
#       'id_history' : cek.id,
#       'id_roles': cek.id_roles,
#       'id_page': cek.id_page,
#       'c': cek.c, 
#       'r': cek.r,
#       'u': cek.u,
#       'd': cek.d,
#       'created_by': cek.created_by, 'created_date': cek.created_date, 'status_aktif': cek.status_aktif,
#     })
#     db.session.add(MAKSESHIST(**insert_history))
#     db.session.commit()
#     ##### Update data di tabel Main #####
#     data_edit = {
#       'id_roles': cek.id_roles,
#       'id_page': cek.id_page,
#       'c': cek.c, 
#       'r': cek.r,
#       'u': cek.u,
#       'd': cek.d,
#       'created_by': 'API', 'created_date': datetime.now(), 'status_aktif': 1,
#     }
#     print(data_edit)
#     db.session.query(MAKSES).filter(MAKSES.id==id).update(data_edit)
#     db.session.commit()

#     ##### Menampilkan data yang di delete #####
#     db.session.close()
#     return jsonify({'status':'success', 'message':'Berhasil update data Master Akses', 'data':data_edit})
#   except Exception as e:
#     print(e)
#     return jsonify({'status':'error', 'message':str(e)})
