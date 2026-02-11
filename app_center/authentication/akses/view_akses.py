from flask.helpers import flash
from app_center.authentication.akses import app_akses, controller_akses, model_akses
from app_center.authentication.akses import controller_akses
from flask import render_template, redirect, url_for, request, jsonify

''' MASTER ROLES '''
@app_akses.route('/api/akses', methods=['GET'])
@controller_akses.autentikasi
def api_akses():
  if request.method == 'GET':
    return controller_akses.getSession()
