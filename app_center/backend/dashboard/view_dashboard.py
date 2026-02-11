from flask.helpers import flash
from app_center.backend.dashboard import be_dashboard_init, controller_dashboard
from app_center.authentication.akses import controller_akses
from flask import render_template, redirect, url_for, request, jsonify

''' AVAIL SURABAYA '''
@be_dashboard_init.route('/api/dashboard-oven-moule', methods=['GET', 'POST', 'PUT', 'DELETE'])
@controller_akses.autentikasi
def api_dashboard_oven_moule():
  mode = request.form.get('mode')
  # if request.method == 'POST' and mode=='graph':
  #   return controller_dashboard.fetchDataDashboard()
    # return controller_dashboard.getAvailabilityAll()
  # elif request.method == 'POST' and mode=='performance':
  #   return controller_oee.getPerformanceAll()
  # elif request.method == 'POST' and mode=='quality':
  #   return controller_oee.getQualityAll()