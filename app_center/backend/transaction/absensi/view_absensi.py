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


''' TRANSACTION IZIN '''
@be_absensi_init.route('/api/t-izin', methods=['GET', 'POST', 'PUT', 'DELETE'])
@controller_akses.autentikasi
def api_t_izin():
  mode = request.form.get('mode')
  if request.method == 'POST' and mode == 'datatable':
    return controller_absensi.getTransAbsensiDatatable()
  

''' TRANSACTION IZIN KELUAR MASUK '''
@be_absensi_init.route('/api/t-izin-keluar-masuk', methods=['GET', 'POST', 'PUT', 'DELETE'])
@controller_akses.autentikasi
def api_t_izin_keluar_masuk():
  if request.is_json:
    payload = request.get_json(silent=True) or {}
    mode = payload.get('mode')
  else:
    mode = request.form.get('mode')

  if request.method == 'POST' and mode == 'datatable':
    return controller_absensi.getTxIzinKeluarMasukDatatable()
  elif request.method == 'POST' and mode == 'add_scan':
    return controller_absensi.addTxIzinKeluarMasuk()
  elif request.method == 'POST' and mode == 'add_manual':
    return controller_absensi.addTxIzinKeluarMasukManual()

  return jsonify({'status': 'error', 'message': 'Mode tidak dikenali atau request tidak valid'})