from flask.helpers import flash
from app_center.modules import controller_module
from app_center.authentication.login import app_login_init, controller, model
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from datetime import datetime
from app_center.authentication.login import model
import requests, json
from app_center.api import controller_api
from app_center.authentication.akses import controller_akses

# ''' DEFAULT URL '''
@app_login_init.route('/')
def route_default():
  """ Routing default url """
  return redirect(url_for('login.login'))

''' VIEW LOGIN '''
@app_login_init.route('/login')
# @minify_decorators.minify(html=True, js=True, cssless=True)
def login():
  """ Routing halaman login """
  if(current_user.is_authenticated == True and current_user.id_role != None):
    return redirect(url_for('fe_master.access_management'))
  elif(current_user.is_authenticated == True and current_user.id_role == None):
    return render_template('accounts/user-akses.html')
  else:
    return render_template('accounts/login.html')
  # if(current_user.is_authenticated == True):
  #   return redirect(url_for('home.home'))
  # else:
  #   return render_template('accounts/login.html')

@app_login_init.route('/login', methods=['POST'])
# @minify_decorators.minify(html=True, js=True, cssless=True)
def login_post():
  """ 
  Routing untuk memproses session login.
  Apabila berhasil login akan langsung dialihkan ke halaman home 
  """
  render_self = controller.loginPost()
  if render_self == True :
    return render_template('accounts/login.html') 
  else:
    return redirect(url_for('login.login'))

''' PROSES LOGIN '''
@app_login_init.route('/api/login', methods=['POST', 'GET'])
def api_login():
  return controller.login()

''' PROSES LOGOUT '''
@app_login_init.route('/api/logout', methods=['POST', 'GET'])
def api_logout():
  return controller.logout()

''' PROSES REGISTRASI '''
@app_login_init.route('/api/registrasi', methods=['POST', 'GET'])
def api_registasi():
  return controller.registrasi()

''' PROSES RESET PASSWORDS '''
@app_login_init.route('/api/forgot-password', methods=['POST', 'GET'])
def api_forgot_password():
  return controller.registrasi()


''' PROSES GET TOKEN '''
@app_login_init.route('/api/bearer-token', methods=['POST'])
def get_token():
  raw_data = request.get_data()
  json_data = json.loads(raw_data.decode('utf-8'))
  if 'nik' not in json_data:
    return jsonify({'message': 'username Tidak Ditemukan !', 'penulisan_variable':'username'})
  if 'password' not in json_data:
    return jsonify({'message': 'password Tidak Ditemukan !', 'penulisan_variable':'password'})
  user_dev = model.User.query.filter(model.User.nik==json_data['nik'], model.User.password==json_data['password'], 
                                     model.User.password!='SSO', model.User.id_role=='1', model.User.status_aktif==1).first()
  if user_dev:
    authentication = controller_module.generateBearerToken(nik_user=json_data['nik'])
    expired = datetime.now().replace(hour=23, minute=59, second=59).strftime('%d/%m/%Y %H:%M:%S GMT+7')
    json_auth = {'message': 'Success!',
                'Authentication':authentication.replace("Bearer ", ""),
                'expiry': expired}
    return jsonify(json_auth)
  sso = controller_api.getSSO(json_data['nik'], json_data['password'])
  if sso == 'T':
    return jsonify({'status':'warning', 'message': 'Password SSO Salah!'})
  elif sso == 'X':
    return jsonify({'status':'warning', 'message': 'Password SSO Kadaluarsa, Harap Ganti Password SSO Anda!'})
  elif sso == 'Z':
    return jsonify({'status':'warning', 'message': 'Nik Tidak Terdaftar Kedalam SSO!'})
  authentication = controller_module.generateBearerToken(nik_user=json_data['nik'])
  expired = datetime.now().replace(hour=23, minute=59, second=59).strftime('%d/%m/%Y %H:%M:%S GMT+7')
  json_auth = {'message': 'Success!',
               'Authentication':authentication.replace("Bearer ", ""),
               'expiry': expired}
  return jsonify(json_auth)






# ''' CRUD MASTER ROLES -- JARE RIAN GAWE NENG KENE WAE.'''


# @app_login_init.route('/api/get-roles-id', methods=['POST'])      ## URL-Param
# def get_roles_id():
#   return controller.get_roles_id()

# @app_login_init.route('/api/add-roles', methods=['POST'])         ## Form-data
# def add_roles():
#   return controller.add_roles()

# @app_login_init.route('/api/delete-roles-id', methods=['DELETE']) ## URL-Param
# def delete_roles_id():
#   return controller.delete_roles_id()

# @app_login_init.route('/api/update-roles-id', methods=['POST'])   ## Form-data
# def update_roles_id():
#   return controller.update_roles_id()



# ''' CRUD MASTER AKSES -- JARE RIAN GAWE NENG KENE WAE.'''
# @app_login_init.route('/api/get-all-akses', methods=['GET'])
# def get_all_akses():
#   return controller.get_akses()

# @app_login_init.route('/api/get-akses-id', methods=['POST'])      ## URL-Param
# def get_akses_id():
#   return controller.get_akses_id()

# @app_login_init.route('/api/add-akses', methods=['POST'])         ## Form-data
# def add_akses():
#   return controller.add_akses()

# @app_login_init.route('/api/delete-akses-id', methods=['DELETE']) ## URL-Param
# def delete_akses_id():
#   return controller.delete_akses_id()

# @app_login_init.route('/api/update-akses-id', methods=['POST'])   ## Form-data
# def update_akses_id():
#   return controller.update_akses_id()

''' CRUD MASTER AKSES -- JARE RIAN GAWE NENG KENE WAE.'''
@app_login_init.route('/api/get-access-management', methods=['GET', 'POST'])
def get_access_management():
  rm = True if request.method == 'POST' else False
  mode = request.form.get('mode')
  if rm and mode == 'datatable':
    return controller.getAksesDatatable()
  else:
    return controller.get_akses()























# ''' PROSES LOGOUT '''
# @app_login_init.route('/logout')
# @login_required
# def logout():
#   """ 
#   Routing untuk memproses session logout.
#   Apabila berhasil logout akan langsung dialihkan ke halaman login 
#   """
#   logout_user()
#   return redirect(url_for('login.logout'))

# # REGISTER
# @app_login_init.route('/register', methods=['POST', 'GET'])
# def register():
#   msg = ''
#   nik = request.form.get('nik_daftar')
#   nama = request.form.get('nama_daftar')
#   password = request.form.get('password_daftar')
  
#   user = model.User.query.filter_by(nik=nik).first()
  
#   if user:
#     return 'user sudah ada'
  
#   # new_user = model.User(nik=nik, nama=nama, password=generate_password_hash(password, method='sha256'))
#   new_user = model.User(nik=nik, nama=nama, password=password)
  
#   # add the new user to the database
#   db.session.add(new_user)
#   db.session.commit() 
  
#   msg='Berhasil Mendaftar'
#   return render_template('login/login.html', msg=msg)


""" PRODUCTION USER WITH ERROR """

''' ERROR HANDLING 403 '''
@app_login_init.errorhandler(403)
def access_forbidden(error):
  return render_template('home/page-403.html'), 403

''' ERROR HANDLING 404 '''
@app_login_init.errorhandler(404)
def not_found_error(error):
  return render_template('home/page-404.html'), 404

''' ERROR HANDLING 500 '''
@app_login_init.errorhandler(500)
def internal_error(error):
  return render_template('home/page-500.html'), 500