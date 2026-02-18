from flask.helpers import flash
from app_center.api import controller_api
from app_center.authentication.akses import controller_akses
from app_center.backend.transaction.lembur import be_lembur_init, controller_lembur
from flask import render_template, redirect, url_for, request, jsonify


''' TRANSACTION LEMBUR '''
@be_lembur_init.route('/api/t-lembur', methods=['GET', 'POST', 'PUT', 'DELETE'])
@controller_akses.autentikasi
def api_t_lembur():
  mode = request.form.get('mode')
  if request.method == 'POST' and mode == 'datatable':
    return controller_lembur.getTransLemburDatatable()
  elif request.method == "POST":
    return controller_lembur.addTransLembur()
  elif request.method == "PUT":
    return controller_lembur.editTransLembur()
  elif request.method == "DELETE":
    return controller_lembur.deleteTransLembur()