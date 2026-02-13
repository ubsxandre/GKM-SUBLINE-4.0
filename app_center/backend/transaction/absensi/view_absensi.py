from flask.helpers import flash
from app_center.api import controller_api
from app_center.authentication.akses import controller_akses
from app_center.backend.transaction.absensi import be_absensi_init, controller_absensi
from flask import render_template, redirect, url_for, request, jsonify


''' TRANSACTION ABSENSI '''
@be_absensi_init.route('/api/t-absensi', methods=['GET', 'POST', 'PUT', 'DELETE'])
@controller_akses.autentikasi
def api_t_absensi():
  mode = request.form.get('mode')
  if request.method == 'POST' and mode == 'datatable':
    return controller_absensi.getTransAbsensiDatatable()