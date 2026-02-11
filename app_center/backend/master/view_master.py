from flask.helpers import flash
from app_center.backend.master import be_master_init, controller_master, model_master
from app_center.authentication.akses import controller_akses
from flask import render_template, redirect, url_for, request, jsonify


''' MASTER ROLES '''
@be_master_init.route('/api/m-roles', methods=['GET', 'POST', 'PUT', 'DELETE'])
@controller_akses.autentikasi
def api_m_roles():
  mode = request.form.get('mode')
  if request.method == 'POST' and mode == 'datatable':
    return controller_master.getRolesDatatable()
  elif request.method == 'POST' and mode == 'dropdown':
    return controller_master.dropdownRoles()
  elif request.method == 'GET':
    return controller_master.getRole()
  elif request.method == 'POST':
    return controller_master.addRole()
  elif request.method == 'PUT':
    return controller_master.editRole()
  elif request.method == 'DELETE':
    return controller_master.deleteRole()

''' MASTER PAGES '''
@be_master_init.route('/api/m-pages', methods=['GET', 'POST', 'PUT', 'DELETE'])
@controller_akses.autentikasi
def api_m_pages():
  mode = request.form.get('mode')
  if request.method == 'POST' and mode == 'datatable':
    return controller_master.getPagesDatatable()
  elif request.method == 'POST' and mode == 'dropdown':
    return controller_master.dropdownPages()
  elif request.method == 'GET':
    return controller_master.getPage()
  elif request.method == 'POST':
    return controller_master.addPage()
  elif request.method == 'PUT':
    return controller_master.editPage()
  elif request.method == 'DELETE':
    return controller_master.deletePage()
  
''' MASTER AKSES '''
@be_master_init.route('/api/m-akses', methods=['GET', 'POST', 'PUT', 'DELETE'])
@controller_akses.autentikasi
def api_m_akses():
  mode = request.form.get('mode')
  if request.method == 'POST' and mode == 'datatable':
    return controller_master.getAksesDatatable()
  elif request.method == 'POST' and mode == 'dropdown_pagses':
    return controller_master.dropdownPagesAtAkses()
  elif request.method == 'POST' and mode == 'dropdown_akseses':
    return controller_master.dropdownAksesAtAkses()
  elif request.method == 'POST' and mode == 'dropdown':
    return controller_master.dropdownAkses()
  elif request.method == 'GET':
    return controller_master.getAkses()
  elif request.method == 'POST':
    return controller_master.addAkses()
  elif request.method == 'PUT':
    return controller_master.editAkses()
  elif request.method == 'DELETE':
    return controller_master.deleteAkses()


''' MASTER AKSES MANAGEMENT '''
@be_master_init.route('/api/m-akses-management', methods=['GET', 'POST', 'PUT', 'DELETE'])
@controller_akses.autentikasi
def api_m_akses_management():
  mode = request.form.get('mode')
  if request.method == 'POST' and mode == 'datatable':
    return controller_master.getAksesManagementDatatable()
  elif request.method == 'GET':
    return controller_master.getAksesManagement()
  # elif request.method == 'POST':
  #   return controller_master.addAksesManagement()
  elif request.method == 'PUT':
    return controller_master.editAksesManagement()
  elif request.method == 'DELETE':
    return controller_master.deleteAksesManagement()
  
''' MASTER BAGIAN '''
@be_master_init.route('/api/m-bagian', methods=['GET', 'POST', 'PUT', 'DELETE'])
@controller_akses.autentikasi
def api_m_bagian():
  mode =request.form.get('mode')
  if request.method == "POST" and mode == "datatable":
    return controller_master.getMasterBagianDatatable()
  elif request.method == 'POST' and mode == 'dropdown':
    return controller_master.dropdownBagian()
  elif request.method == "POST":
    return controller_master.addMasterBagian()
  elif request.method == "PUT":
    return controller_master.editMasterBagian()
  elif request.method == "DELETE":
    return controller_master.deleteMasterBagian()
  elif request.method == "GET":
    return controller_master.getMasterBagian()

# ''' MASTER DEPARTEMEN '''
# @be_master_init.route('/api/m-departemen', methods=['GET', 'POST', 'PUT', 'DELETE'])
# @controller_akses.autentikasi
# def api_m_departemen():
#   mode =request.form.get('mode')
#   if request.method == "POST" and mode == "datatable":
#     return controller_master.getMasterDepartemenDatatable()
#   elif request.method == "POST":
#     return controller_master.addMasterDepartemen()
#   elif request.method == "PUT":
#     return controller_master.editMasterDepartemen()
#   elif request.method == "DELETE":
#     return controller_master.deleteMasterDepartemen()
#   elif request.method == "GET":
#     return controller_master.getMasterDepartemen()
  