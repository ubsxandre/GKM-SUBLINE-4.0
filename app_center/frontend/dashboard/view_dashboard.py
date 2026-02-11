from flask.helpers import flash
from app_center.frontend.dashboard import fe_dashboard_init
from app_center.authentication.akses import controller_akses
from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user

''' DASHBOARD OVEN MOULE '''
# @fe_dashboard_init.route('/dashboard-oven-moule')
# @login_required
# @controller_akses.cek_page('DASHBOARD OVEN MOULE')
# @controller_akses.page_counter('dashboard-oven-moule')
# def dashboard_oven_moule():
#   """ Routing Dashboard Oven Moule"""
#   return render_template('dashboard/dashboard-oven-moule.html', page="dashboard-oven-moule")