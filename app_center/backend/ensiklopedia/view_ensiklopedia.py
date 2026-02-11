from flask.helpers import flash
from app_center.backend.ensiklopedia import be_ensiklopedia_init, controller_ensiklopedia
from app_center.authentication.akses import controller_akses
from flask import render_template, redirect, url_for, request, jsonify

'''ENSIKLOPEDIA'''
@be_ensiklopedia_init.route('/api/ensiklopedia', methods=['GET', 'POST', 'PUT', 'DELETE'])
def view_api_ensiklopedia():
  if request.method == 'POST':
    return controller_ensiklopedia.addEnsiklopedia()
  elif request.method == 'GET':
    return controller_ensiklopedia.getEnsiklopedia()
  elif request.method == 'DELETE':
    return controller_ensiklopedia.deleteEnsiklopedia()