from flask.helpers import flash
from app_center.backend.influx import be_influx_init, model_influx, controller_influx
from app_center.authentication.akses import controller_akses
from flask import render_template, redirect, url_for, request, jsonify


''' ASD '''
@be_influx_init.route('/api/get-raw-merge', methods=['GET', 'POST', 'PUT', 'DELETE'])
@controller_akses.autentikasi
def api_get_raw_merge():
  mode = request.form.get('mode')
  # if request.method == 'POST':
  #   controller_influx.getRawMergeOven(no_mesin='', sd='', ed='')
 