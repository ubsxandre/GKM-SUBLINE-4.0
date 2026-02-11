from flask.helpers import flash
from app_center.backend.testing import be_testing_init, controller_testing, model_testing
from app_center.websocket import controller_websocket
from flask import render_template, redirect, url_for, request, jsonify
from datetime import datetime, timedelta
import json, os, pandas as pd, numpy as np


''' UGAL UGAL AN . ##### INI HANYA SEMENTARA, TETAP TABAH, TAWAKAL DAN JANGAN DI HAPUS'''
from app_center.backend.master import model_master, controller_master
from app_center.backend.transaction.oven_siklus import controller_oven_siklus
from app_center.api import controller_api
from app_center.backend.influx import controller_influx


@be_testing_init.route('/api/testing', methods=['GET'])
def api_testing():
  mode = request.form.get('mode')
  if request.method == 'GET':
    controller_influx.getRawDataOvenMoule(no_mesin='', sd='', ed='')
    return 'asd'
    # return render_template('testing/testing-websocket.html', page="testing-websocket")



''' TESTING WEBSOC '''
@be_testing_init.route('/api/tes-web-soc', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_tes_web_soc():
  # controller_websocket.getDataWebsocLantai3()
  return render_template('testing/testing-websocket.html', page="testing-websocket")
  

''' TESTING TELEGRAM '''
@be_testing_init.route('/api/telegram', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_telegram():
  
  pesan = f"Halo, saya chat bot dari <b>TEAM 4.0</b>"
  result = controller_testing.send_message(pesan)

  if result.get('ok'):
    return 'Pesan berhasil dikirim ke Telegram ✅', 'success'
  else:
    return (f"Gagal mengirim pesan ❌: {result.get('error')}", 'danger')

