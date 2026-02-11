from flask.helpers import flash
from app_center.frontend.login import fe_login_init
from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user

# ''' DEFAULT URL '''
# @fe_login_init.route('/')
# def route_default():
#   """ Routing default url """
#   return redirect(url_for('fe_login.login'))

# ''' VIEW LOGIN '''
# @fe_login_init.route('/login', methods=['POST', 'GET'])
# def login():
#   """ Routing halaman login """
#   if(current_user.is_authenticated == True and current_user.id_role != None):
#     return redirect(url_for('fe_dashboard.dashboard_oee'))
#   elif(current_user.is_authenticated == True and current_user.id_role == None):
#     return render_template('accounts/user-akses.html')
#   else:
#     return render_template('accounts/login.html')

# ''' VIEW REGISTER '''
# @fe_login_init.route('/registrasi')
# def registrasi():
#   """ Routing halaman registrasi """
#   return render_template('accounts/registrasi.html')