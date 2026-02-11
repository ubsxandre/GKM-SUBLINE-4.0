from flask.helpers import flash
from app_center.frontend.ensiklopedia import fe_ensiklopedia_init
from app_center.authentication.akses import controller_akses
from flask import render_template, redirect, url_for, request, abort
from flask_login import login_user, login_required, current_user, logout_user

''' ENSIKLOPEDIA '''
@fe_ensiklopedia_init.route('/ensiklopedia')
@login_required
@controller_akses.cek_page('ENSIKLOPEDIA')
@controller_akses.page_counter('ensiklopedia')
def ensiklopedia():
  """ Routing ENSIKLOPEDIA"""
  return render_template('ensiklopedia/ensiklopedia.html', page="ensiklopedia")
