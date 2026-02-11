from flask.helpers import flash
from app_center.api import controller_api
from app_center.authentication.akses import controller_akses
from app_center.backend.transaction.oven_siklus import be_oven_siklus_init, controller_oven_siklus
from flask import render_template, redirect, url_for, request, jsonify

''' TRANSACTION OVEN SIKLUS '''
@be_oven_siklus_init.route('/api/t-oven-siklus', methods=['GET', 'POST', 'PUT', 'DELETE'])
@controller_akses.autentikasi
def api_t_oven_siklus():
  mode = request.form.get('mode')
  # if request.method == 'POST' and mode == 'datatable':
  #   return controller_oven_siklus.getTxOvenSiklusDatatable()
  # elif request.method == 'POST':
  #   return controller_oven_siklus.addTxOvenSiklus()
  # elif request.method == 'PUT':
  #   return controller_oven_siklus.editTxOvenSiklus()
  # elif request.method == 'DELETE':
  #   return controller_oven_siklus.deleteTxOvenSiklus()