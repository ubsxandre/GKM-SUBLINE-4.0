from flask.helpers import flash
from app_center.frontend.testing import fe_testing_init
from app_center.authentication.akses import controller_akses
from flask import render_template, redirect, url_for, request, abort
from flask_login import login_user, login_required, current_user, logout_user

''' TESTING TELEGRAM '''
@fe_testing_init.route('/testing-telegram')
def testing_telegram():
  return render_template('testing/testing-telegram.html', page="testing-telegram")