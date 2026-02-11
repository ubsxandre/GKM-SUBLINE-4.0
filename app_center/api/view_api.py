from flask.helpers import flash
from app_center.api import app_api, controller_api, model_api
from flask import render_template, redirect, url_for, request, jsonify

# ''' API QC PRODUKSI '''
# @app_api.route('/api/data-qc-produksi', methods=['GET','POST'])
# def api_data_qc_produksi():
#   mode = request.form.get('mode')
#   if request.method == 'POST' and mode == 'qc_produksi':
#     return controller_api.getQcProduksi()
  

# ''' API POST QC PRODUKSI '''
# @app_api.route('/api/post-qc-produksi', methods=['POST'])
# def api_post_qc_produksi():
#   return controller_api.postQCProduksiToSiskom()
  
''' API DEPARTEMEN FROM HCIS'''
@app_api.route('/api/dept-hcis', methods=['GET', 'POST'])
def api_dept_hcis():
  if request.method == 'GET':
    return controller_api.getDepartment()

''' API EMPLOYEE FROM HCIS'''
@app_api.route('/api/employee-hcis', methods=['GET', 'POST'])
def api_employee_hris():
  if request.method == 'GET':
    nik = request.args.get('nik')
    return controller_api.getEmployeeHCIS(nik)

''' API SUBDEPARTEMEN FROM HCIS'''
@app_api.route('/api/subdepartemen-hcis', methods=['GET', 'POST'])
def api_subdepartemen_hcis():
  if request.method == 'GET':
    nik = request.args.get('nik')
    return controller_api.getSubDepartmentHCIS()

''' API JABATAN DEPARTEMEN FROM HCIS'''
@app_api.route('/api/jabatan-departemen-hcis', methods=['GET', 'POST'])
def api_jabatan_departemen_hris():
  if request.method == 'GET':
    search = request.args.get("search")
    return controller_api.getHCISJabatan(search)

''' API AUTO COMPLETE FROM HCIS'''
@app_api.route('/api/auto-complete-hcis', methods=['GET', 'POST'])
def api_auto_complete_hcis():
  if request.method == 'GET':
    search = request.args.get("search")
    return controller_api.getHCISKarAutoComplete(search)