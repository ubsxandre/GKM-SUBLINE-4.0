from flask.helpers import flash
from app_center.backend.master import model_master
from app_center.authentication.login import model
from flask import render_template, redirect, url_for, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app_center import db
from flask_login import login_user, login_required, current_user, logout_user
from flask_minify import Minify, decorators as minify_decorators
from app_center.authentication.akses import controller_akses
from app_center.api import controller_api
from sqlalchemy import func, case, and_, or_, cast, DATE, INT, literal_column, union_all, inspect
from sqlalchemy.orm import aliased, Session
from datetime import datetime, timedelta, time
from app_center.modules import controller_module
import json, os, pandas as pd, numpy as np

from app_center.websocket import view_websocket


'''' INITIAL MODEL '''
USER = model.User
MROLES = model_master.MasterRoles
MROLESHIST = model_master.MasterRolesHistory
MPAGES = model_master.MasterPages
MPAGESHIST = model_master.MasterPagesHistory
MAKSES = model_master.MasterAkses
MAKSESHIST = model_master.MasterAksesHistory
MAM = model_master.MasterAksesManagement
MAMHIST = model_master.MasterAksesManagementHistory
MBAGIAN = model_master.MasterBagian
MBAGIANHIST = model_master.MasterBagianHistory
MPLOY = model_master.MasterEmployees


def daterange(start_date, end_date):
  for n in range(int((end_date - start_date).days)):
    yield start_date + timedelta(n)


''' Master Roles '''
def getRolesDatatable():
  datatable = controller_module.Datatable(request.form)
  search_value = datatable.get_search_value()
  order = []
 
  sort_col_name = ['id', 'role']
  sort_obj = {
    'id': MROLES.id,
    'role': MROLES.role,
  }
  order = datatable.get_order(sort_col_name=sort_col_name, sort_obj=sort_obj)
  order.append(MROLES.id)

  jumlah_data_full = db.session.query(MROLES).filter(MROLES.status_aktif=='1').count()

  query_filtered = db.session.query(MROLES).with_entities(MROLES.id,
                                                          MROLES.role,)\
                                          .filter(MROLES.status_aktif=='1',
                                                  or_(MROLES.id.like(search_value),
                                                      MROLES.role.like(search_value)))\
                                          .order_by(*order)

  data_json = datatable.get_data_json_with_entities(query_filtered) 
  response = datatable.get_response(jumlah_data_full=jumlah_data_full, data_json=data_json)
  return jsonify(response)

@controller_akses.cek_akses_api('MASTER ROLES-R')
def getRole():
  try:
    id = request.args.get('id')
    role = request.args.get('role')
    filter = []
    filter.append(MROLES.id==id) if id else []
    filter.append(MROLES.role==role) if role else []

    qrole = db.session.query(MROLES).with_entities(MROLES.id, 
                                                  MROLES.role)\
                                .filter(MROLES.status_aktif==1,
                                        *filter,
                                        ).all()    
    data = []
    for row in qrole:
      data.append(row._asdict())
    message = 'Role retrieved successfully' if qrole else 'Role not found' 
    return jsonify({'status':'success', 'message':message, 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})
  
@controller_akses.cek_akses_api('MASTER ROLES-C')
def addRole():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_input = {'created_by' : created_by}
    for row in data:
      data_input[row] = data.get(row)
      
    qcek = db.session.query(MROLES).filter(MROLES.status_aktif=='1',
                                               MROLES.role==data_input['role'],
                                              ).first()     
    if qcek:
      return jsonify({'status':'error', 'message':'Role already exists'})
    
    add = MROLES(**data_input)
    db.session.add(add)
    db.session.commit()

    data = add.to_dict()
    db.session.close()
    return jsonify({'status':'success', 'message':'Role added successfully', 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

@controller_akses.cek_akses_api('MASTER ROLES-U')
def editRole():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_edit = {'created_by' : created_by}    
    for row in data:
      data_edit[row] = data.get(row)

    qcek = db.session.query(MROLES).filter(MROLES.role==data_edit['role'], MROLES.status_aktif == 1).first()
    if qcek:
      return jsonify({'status':'error', 'message':'Role Name already exists'})

    qedit = db.session.query(MROLES).filter(MROLES.id==data_edit['id'], MROLES.status_aktif == 1).first()
    if not qedit:
      return jsonify({'status':'error', 'message':'ID Role not found'})
    data_old = qedit.__dict__

    del data_old['_sa_instance_state']
    del data_old['id']
    data_old['id_history'] = data_edit['id']
    
    db.session.add(MROLESHIST(**data_old))
    db.session.commit()
    
    db.session.query(MROLES).filter(MROLES.id==data_edit['id']).update(data_edit)
    db.session.commit()
    db.session.close()
    return jsonify({'status':'success', 'message':'Role updated successfully', 'data':data_edit})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})
  
@controller_akses.cek_akses_api('MASTER ROLES-D')
def deleteRole():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_delete = {'created_by' : created_by, 'created_date' : datetime.now(), 'status_aktif':0}
    for row in data:
      data_delete[row] = data.get(row)
    qdel = db.session.query(MROLES).filter(MROLES.id==data_delete['id'], MROLES.status_aktif == 1).first()
    if not qdel:
      return jsonify({'status':'error', 'message':'ID Role not found'})
    data_old = qdel.__dict__

    del data_old['_sa_instance_state']
    del data_old['id']
    data_old['id_history'] = data_delete['id']

    delete = MROLESHIST(**data_old)
    db.session.add(delete)
    db.session.commit()

    db.session.query(MROLES).filter(MROLES.id==data_delete['id'], MROLES.status_aktif == 1)\
      .update(data_delete)
    db.session.commit()
    
    data = delete.to_dict()

    return jsonify({'status':'success', 'message':'Role deleted successfully', 'data':data})
    
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})
  

''' Master Page '''
def getPagesDatatable():
  datatable = controller_module.Datatable(request.form)
  search_value = datatable.get_search_value()
  order = []
 
  sort_col_name = ['page', 'crud']
  sort_obj = {
    'page': MPAGES.page,
    'crud': MPAGES.crud,
  }
  order = datatable.get_order(sort_col_name=sort_col_name, sort_obj=sort_obj)
  order.append(MPAGES.id)

  jumlah_data_full = db.session.query(MPAGES).filter(MPAGES.status_aktif=='1').count()

  query_filtered = db.session.query(MPAGES).with_entities(MPAGES.id,
                                                          MPAGES.page,
                                                          MPAGES.crud,)\
                                          .filter(MPAGES.status_aktif=='1',
                                                  or_(MPAGES.page.like(search_value),
                                                      MPAGES.crud.like(search_value)))\
                                          .order_by(*order)

  data_json = datatable.get_data_json_with_entities(query_filtered) 
  response = datatable.get_response(jumlah_data_full=jumlah_data_full, data_json=data_json)
  return jsonify(response)

@controller_akses.cek_akses_api('MASTER PAGES-R')
def getPage():
  try:
    id = request.args.get('id')
    page = request.args.get('page')
    filter = []
    filter.append(MPAGES.id==id) if id else []
    filter.append(MPAGES.page==page) if page else []

    qpage = db.session.query(MPAGES).with_entities(MPAGES.id, 
                                                  MPAGES.crud,
                                                  MPAGES.page)\
                                .filter(MPAGES.status_aktif==1,
                                        *filter,
                                        ).all()    
    data = []
    for row in qpage:
      data.append(row._asdict())
    message = 'Page retrieved successfully' if qpage else 'Page not found' 
    return jsonify({'status':'success', 'message':message, 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

@controller_akses.cek_akses_api('MASTER PAGES-C')
def addPage():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_input = {'created_by':created_by}
    for row in data:
      data_input[row] = data.get(row)
    breakdown = []
    for crot in data_input['crud'].split(","):
      obj = {}
      obj.update(data_input)
      obj['crud'] = crot
      breakdown.append(obj)
    data_message = []
    ff, gg = 0, 0
    for wor in breakdown:
      ff += 1
      qcek = db.session.query(MPAGES).filter(MPAGES.status_aktif==1, MPAGES.page==wor['page'], MPAGES.crud==wor['crud']).first()
      if qcek:
        gg += 1
        obj = {}
        obj.update(wor)
        obj['description'] = 'failed'
        data_message.append(obj)
      else:
        add = MPAGES(**wor)
        db.session.add(add)
        db.session.commit()
        obj = {}
        obj.update(add.to_dict())
        obj['description'] = 'success'
        data_message.append(obj)
    db.session.close()    
    if gg == ff:
      return jsonify({'status':'error', 'message':'Page already exists', 'data':data_message})  
    return jsonify({'status':'success', 'message':'Page added successfully', 'data':data_message})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})
  
@controller_akses.cek_akses_api('MASTER PAGES-U')
def editPage():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_edit = {'created_by' : created_by,}
    for row in data:
      data_edit[row] = data.get(row)

    qcek = db.session.query(MPAGES).filter(MPAGES.page==data_edit['page'], MPAGES.status_aktif == 1).first()
    if qcek:
      return jsonify({'status':'error', 'message':'Page Name already exists'})

    qedit = db.session.query(MPAGES).filter(MPAGES.id==data_edit['id'], MPAGES.status_aktif == 1).first()
    if not qedit:
      return jsonify({'status':'error', 'message':'ID Page not found'})
    data_old = qedit.__dict__

    del data_old['_sa_instance_state']
    del data_old['id']
    data_old['id_history'] = data_edit['id']
    
    db.session.add(MPAGESHIST(**data_old))
    db.session.commit()
    
    db.session.query(MPAGES).filter(MPAGES.id==data_edit['id']).update(data_edit)
    db.session.commit()
    db.session.close()
    return jsonify({'status':'success', 'message':'Page updated successfully', 'data':data_edit})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

@controller_akses.cek_akses_api('MASTER PAGES-D')
def deletePage():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_delete = {'created_by' : created_by, 'created_date' : datetime.now(), 'status_aktif':0}
    for row in data:
      data_delete[row] = data.get(row)

    qdel = db.session.query(MPAGES).filter(MPAGES.id==data_delete['id'], MPAGES.status_aktif == 1).first()
    if not qdel:
      return jsonify({'status':'error', 'message':'ID Page not found'})
    data_old = qdel.__dict__

    del data_old['_sa_instance_state']
    del data_old['id']
    data_old['id_history'] = data_delete['id']

    delete = MPAGESHIST(**data_old)
    db.session.add(delete)
    db.session.commit()

    db.session.query(MPAGES).filter(MPAGES.id==data_delete['id'], MPAGES.status_aktif == 1)\
      .update(data_delete)
    db.session.commit()
    
    data = delete.to_dict()

    return jsonify({'status':'success', 'message':'Page deleted successfully', 'data':data})
    
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})


''' Master Akses '''
def getAksesDatatable():
  datatable = controller_module.Datatable(request.form)
  search_value = datatable.get_search_value()
  order = []
 
  sort_col_name = ['role', 'page', 'akses']
  sort_obj = {
    'role': MROLES.role,
    'page': MPAGES.page,
    'akses': MAKSES.akses,
  }
  order = datatable.get_order(sort_col_name=sort_col_name, sort_obj=sort_obj)
  order.append(MROLES.role)
  order.append(MPAGES.page)

  jumlah_data_full = db.session.query(MAKSES).join(MROLES, MAKSES.id_role==MROLES.id)\
                                            .join(MPAGES, MAKSES.id_page==MPAGES.id)\
                                            .filter(MAKSES.status_aktif=='1').count()

  query_filtered = db.session.query(MAKSES).join(MROLES, MAKSES.id_role==MROLES.id)\
                                          .join(MPAGES, MAKSES.id_page==MPAGES.id)\
                                          .with_entities(MAKSES.id,
                                                          MROLES.role,
                                                          MPAGES.page,  
                                                          MAKSES.id_role,
                                                          MAKSES.id_page,
                                                          MAKSES.akses,)\
                                          .filter(MAKSES.status_aktif=='1',
                                                  or_(MROLES.role.like(search_value),
                                                      MPAGES.page.like(search_value),
                                                      MAKSES.akses.like(search_value),))\
                                          .order_by(*order)

  data_json = datatable.get_data_json_with_entities(query_filtered) 
  response = datatable.get_response(jumlah_data_full=jumlah_data_full, data_json=data_json)
  return jsonify(response)

@controller_akses.cek_akses_api('MASTER ACCESS-R')
def getAkses():
  try:
    id = request.args.get('id')
    id_role = request.args.get('id_role')
    id_page = request.args.get('id_page')
    akses = request.args.get('akses')
    filter = []
    filter.append(MAKSES.id==id) if id else []
    filter.append(MAKSES.id_role==id_role) if id_role else []
    filter.append(MAKSES.id_page==id_page) if id_page else []
    filter.append(MAKSES.akses==akses) if akses else []

    qakses = db.session.query(MAKSES).with_entities(
                                        MAKSES.id, 
                                        MAKSES.id_role, MAKSES.id_page,
                                        MROLES.role, MPAGES.page,
                                        MAKSES.akses,
                                      )\
                                      .join(MPAGES, and_(MPAGES.id==MAKSES.id_page, MPAGES.status_aktif==1))\
                                      .join(MROLES, and_(MROLES.id==MAKSES.id_role, MROLES.status_aktif==1))\
                                      .filter(MAKSES.status_aktif==1,
                                              *filter
                                              ).all()
    data = []
    for row in qakses:
      data.append(row._asdict())
    message = 'Access retrieved successfully' if qakses else 'Access not found' 
    return jsonify({'status':'success', 'message':message, 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

@controller_akses.cek_akses_api('MASTER ACCESS-C')
def addAkses():
  try:    
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_input = {'created_by' : created_by}
    for row in data:
      data_input[row] = data.get(row)
    breakdown = []
    i = 0
    for crot in data_input['akses'].split(","):
      obj = {}
      obj.update(data_input)
      obj['akses'] = crot
      obj['id_page'] = data_input['id_page'].split(",")[i]
      i += 1
      breakdown.append(obj)
    data_message = []
    ff, gg = 0, 0
    for wor in breakdown:
      ff += 1
      qcek = db.session.query(MAKSES).filter(MAKSES.status_aktif==1, MAKSES.id_page==wor['id_page'], 
                                            MAKSES.id_role==wor['id_role'], MAKSES.akses==wor['akses']).first()
      if qcek:
        gg += 1
        obj = {}
        obj.update(wor)
        obj['description'] = 'failed'
        data_message.append(obj)
      else:
        add = MAKSES(**wor)
        db.session.add(add)
        db.session.commit()
        obj = {}
        obj.update(add.to_dict())
        obj['description'] = 'success'
        data_message.append(obj)
    db.session.close()    
    if gg == ff:
      return jsonify({'status':'error', 'message':'Access already exists', 'data':data_message})  
    return jsonify({'status':'success', 'message':'Access added successfully', 'data':data_message})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

@controller_akses.cek_akses_api('MASTER ACCESS-U')
def editAkses():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_edit = {'created_by' : created_by}
    for row in data:
      data_edit[row] = data.get(row)
    qcek = db.session.query(MAKSES).filter( MAKSES.status_aktif == 1,
                                            MAKSES.id_page==data_edit['id_page'], MAKSES.id_role==data_edit['id_role'], 
                                            MAKSES.akses==data_edit['akses'],).first()
    if qcek:
      return jsonify({'status':'error', 'message':'Access Name already exists'})

    qedit = db.session.query(MAKSES).filter(MAKSES.id==data_edit['id'], MAKSES.status_aktif == 1).first()
    if not qedit:
      return jsonify({'status':'error', 'message':'ID Access not found'})
    data_old = qedit.__dict__

    del data_old['_sa_instance_state']
    del data_old['id']
    data_old['id_history'] = data_edit['id']
    
    db.session.add(MAKSESHIST(**data_old))
    db.session.commit()
    
    db.session.query(MAKSES).filter(MAKSES.id==data_edit['id']).update(data_edit)
    db.session.commit()
    db.session.close()
    return jsonify({'status':'success', 'message':'Access updated successfully', 'data':data_edit})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

@controller_akses.cek_akses_api('MASTER ACCESS-D')
def deleteAkses():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_delete = {'created_by' : created_by, 'created_date' : datetime.now(), 'status_aktif':0}
    for row in data:
      data_delete[row] = data.get(row)
    qdel = db.session.query(MAKSES).filter(MAKSES.id==data_delete['id'], MAKSES.status_aktif == 1).first()
    if not qdel:
      return jsonify({'status':'error', 'message':'ID Access not found'})
    data_old = qdel.__dict__

    del data_old['_sa_instance_state']
    del data_old['id']
    data_old['id_history'] = data_delete['id']

    delete = MAKSESHIST(**data_old)
    db.session.add(delete)
    db.session.commit()

    db.session.query(MAKSES).filter(MAKSES.id==data_delete['id'], MAKSES.status_aktif == 1)\
      .update(data_delete)
    db.session.commit()
    
    data = delete.to_dict()
    db.session.close()
    return jsonify({'status':'success', 'message':'Access deleted successfully', 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})
  

''' Akses Management ** Additional Page'''
def getAksesManagementDatatable():
  datatable = controller_module.Datatable(request.form)
  search_value = datatable.get_search_value()
  data = []

  # definisi status
  statusemek = case(
    (and_(USER.id_role == None, USER.status_aktif == '1'), "Pending"),
    (USER.status_aktif == "0", "Inactive"),
    else_="Active"
  )

  # sorting
  sort_col_name = ['nama', 'departemen', 'golongan', 'roles', 'nik', "status"]
  sort_obj = {
    'nama': USER.nama,
    'departemen': USER.departemen,
    'golongan': USER.golongan,
    'roles': MROLES.role,
    'nik': USER.nik,
    'status': statusemek,
  }
  order = datatable.get_order(sort_col_name=sort_col_name, sort_obj=sort_obj)
  order.append(USER.id)  # biar stabil sorting-nya

  # total semua data (tanpa filter)
  total_records = db.session.query(USER).filter(USER.status_aktif == 1).count()

  # query yang difilter
  query_filtered = db.session.query(
    USER.nama, USER.id, USER.departemen, USER.golongan,
    func.date_format(USER.created_date, '%m-%Y').label('created_date'),
    USER.id_role, statusemek.label("status"),
    MROLES.role, USER.nik, USER.status_aktif
  ).outerjoin(
    MROLES, and_(MROLES.id == USER.id_role, USER.status_aktif == 1)
  ).filter(
    USER.status_aktif == 1,
    or_(
      USER.nik.like(search_value),
      USER.nama.like(search_value),
      statusemek.like(search_value),
      USER.departemen.like(search_value),
      MROLES.role.like(search_value),
    )
  ).order_by(*order)

  # ambil data dengan pagination
  users = query_filtered.slice(datatable.row_start, datatable.row_start + datatable.row_per_page).all()
  datatable.jumlah_data_filtered = query_filtered.count()

  # proses data
  for row in users:
    obj = row._asdict()

    # ambil detail akses
    qmam = db.session.query(
      MAM.id, USER.nik, MAM.id_role, MROLES.role,
      MAM.id_page, MPAGES.page, MAM.akses,
      literal_column("'checked'").label('status')
    ).outerjoin(
      MAM, and_(
        MAM.nik == USER.nik,
        MAM.id_role == USER.id_role,
        MAM.status_aktif == 1
      )
    ).join(
      MROLES, and_(MROLES.id == MAM.id_role, MROLES.status_aktif == 1)
    ).join(
      MPAGES, and_(MPAGES.id == MAM.id_page, MPAGES.status_aktif == 1)
    ).filter(
      USER.nik == row.nik,
      USER.status_aktif == 1
    )

    obj['det'] = [item._asdict() for item in qmam.all()]
    data.append(obj)

  return jsonify(datatable.get_response(jumlah_data_full=total_records, data_json=data))


@controller_akses.cek_akses_api('ACCESS MANAGEMENT-R')
def getAksesManagement():
  try:
    nik = request.args.get('nik')
    new_data = []
    filter = []
    filter.append(USER.nik==nik) if nik else []
    
    quser = db.session.query(USER).with_entities(USER.nama, USER.id, USER.departemen, USER.golongan, 
                                              USER.id_role, MROLES.role, USER.nik
                                              )\
                            .outerjoin(MROLES, and_(MROLES.id==USER.id_role, USER.status_aktif==1))\
                            .filter(USER.status_aktif==1,
                                    *filter,
                                    )
    quserall = quser.all()
    for row in quserall:
      obj = {}
      obj.update(row._asdict())
      qmam = db.session.query(USER).with_entities(MAM.id, USER.nik, MAM.id_role, MROLES.role, 
                                                  MAM.id_page, MPAGES.page, MAM.akses, 
                                                  literal_column("'checked'").label('status'), 
                                                  )\
                                                    .outerjoin(MAM, and_(MAM.nik==USER.nik, MAM.id_role==USER.id_role, MAM.status_aktif==1))\
                                                    .join(MROLES, and_(MROLES.id==MAM.id_role, MROLES.status_aktif==1))\
                                                    .join(MPAGES, and_(MPAGES.id==MAM.id_page, MPAGES.status_aktif==1))\
                                                    .filter(USER.status_aktif==1,USER.nik==row.nik)
      qmamall = qmam.all()
      obj['det'] = []
      for wor in qmamall:
        obj['det'].append(wor._asdict())
      new_data.append(obj)     
    message = 'Access Management retrieved successfully' if new_data else 'Access not found' 
    return jsonify({'status':'success', 'message':message, 'data':new_data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

@controller_akses.cek_akses_api('ACCESS MANAGEMENT-U')
def editAksesManagement():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    qcekuser = db.session.query(USER).filter(USER.status_aktif==1, USER.nik==data[0]['nik']).first()
    if not qcekuser:
      return jsonify({'status':'error', 'message':'Nik not found !', 'data':[{'nik':data[0]['nik']}]})
    if qcekuser:
      db.session.query(USER).filter(USER.status_aktif==1, USER.nik==data[0]['nik']).update({'id_role':data[0]['id_role']})
      db.session.commit()
      qmove = db.session.query(MAM).with_entities(MAM.id, MAM.nik, MAM.id_role, MAM.id_page, MAM.akses, MAM.created_by, MAM.created_date, MAM.status_aktif).filter(MAM.nik==data[0]['nik']).all()
      if qmove: 
        data_old = []
        for dor in qmove:
          obj = {}
          obj.update(dor._asdict())
          obj['id_history'] = obj['id']
          del obj['id']
          data_old.append(obj)
          db.session.add(MAMHIST(**obj))
          db.session.commit()
        db.session.query(MAM).filter(MAM.nik==data[0]['nik']).delete()
        db.session.commit()

      data_success = []
      for row in data:
        del [row['page'], row['role'], row['status']]
        row['created_by'] = created_by
        add = MAM(**row)
        db.session.add(add)
        db.session.commit()
        data_success.append(add.to_dict())
    db.session.close()  
    return jsonify({'status':'success', 'message':'Access edited successfully', 'data':data_success})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

@controller_akses.cek_akses_api('ACCESS MANAGEMENT-D')
def deleteAksesManagement():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_delete = {'created_by' : created_by, 'created_date' : datetime.now(), 'status_aktif':0}
    for row in data:
      data_delete[row] = data.get(row)
    qdeluser = db.session.query(USER).filter(USER.status_aktif==1, USER.nik==data_delete['nik']).first()
    if not qdeluser:
      return jsonify({'status':'error', 'message':'NIK not found'})
    del data_delete['id']
    db.session.query(USER).filter(USER.status_aktif==1, USER.nik==data_delete['nik']).update(data_delete)
    db.session.commit()

    qmove = db.session.query(MAM).with_entities(MAM.id, MAM.nik, MAM.id_role, MAM.id_page, MAM.akses, MAM.created_by, MAM.created_date, MAM.status_aktif).filter(MAM.nik==data_delete['nik']).all()
    data_success = []
    if qmove:
      data_old = []
      for dor in qmove:
        obj = {}
        obj.update(dor._asdict())
        obj['id_history'] = obj['id']
        del obj['id']
        data_old.append(obj)
        hapus = MAMHIST(**obj)
        db.session.add(hapus)
        db.session.commit()
      db.session.query(MAM).filter(MAM.nik==data_delete['nik']).delete()
      db.session.commit()   
      data_success.append(hapus.to_dict())
    db.session.close()
    return jsonify({'status':'success', 'message':'Access deleted successfully', 'data':data_success})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})


''' DROP DROP AN '''
def dropdownRoles():
  try:
    qrole = db.session.query(MROLES).with_entities(MROLES.id, 
                                                  MROLES.role)\
                                .filter(MROLES.status_aktif==1,
                                        ).all()    
    data = []
    for row in qrole:
      data.append(row._asdict())
    message = 'Roles retrieved successfully' if qrole else 'Roles not found' 
    return jsonify({'status':'success', 'message':message, 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

def dropdownPages():
  try:
    qpage = db.session.query(MPAGES).with_entities(MPAGES.page)\
                                .filter(MPAGES.status_aktif==1,)\
                                .group_by(MPAGES.page)\
                                .all()    
    data = []
    for row in qpage:
      data.append(row._asdict())
    message = 'Pages retrieved successfully' if qpage else 'Page not found' 
    return jsonify({'status':'success', 'message':message, 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

def dropdownAkses():
  try:
    id_role = request.form.get('id_role')
    id_page = request.form.get('id_page')
    page = request.form.get('page')
    filter = []
    filter.append(MAKSES.id_role==id_role,) if request.form.get('id_role') else filter.append([])
    filter.append(MAKSES.id_page==id_page,) if request.form.get('id_role') else filter.append([])
    filter.append(MPAGES.page==page,) if request.form.get('page') else filter.append([])
    qakses = db.session.query(MAKSES).with_entities(
                                        MAKSES.id, 
                                        MAKSES.id_role, MAKSES.id_page,
                                        MROLES.role, MPAGES.page,
                                        MAKSES.akses,
                                      )\
                                      .join(MPAGES, and_(MPAGES.id==MAKSES.id_page, MPAGES.status_aktif==1))\
                                      .join(MROLES, and_(MROLES.id==MAKSES.id_role, MROLES.status_aktif==1))\
                                      .filter(MAKSES.status_aktif==1,
                                              *filter,
                                              ).all()
    data = []
    for row in qakses:
      data.append(row._asdict())
    message = 'Access retrieved successfully' if qakses else 'Access not found' 
    return jsonify({'status':'success', 'message':message, 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

def dropdownPagesAtAkses():
  try:
    id_role = request.form.get('id_role')

    filter = []
    filter.append(MAKSES.id_role==id_role,) if request.form.get('id_role') else filter.append([])
    
    qexists = db.session.query(MAKSES).with_entities(MAKSES.id).filter(MAKSES.status_aktif==1, MPAGES.id==MAKSES.id_page, *filter).scalar_subquery()
    qpages = db.session.query(MPAGES).with_entities(MPAGES.page)\
                                      .filter(MPAGES.status_aktif==1,
                                              ~func.exists(qexists)
                                              )\
                                      .group_by(MPAGES.page)\
                                      .all()
    data = []
    for row in qpages:
      data.append(row._asdict())
    message = 'Pages retrieved successfully' if qpages else 'Pages not found' 
    return jsonify({'status':'success', 'message':message, 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})
  
def dropdownAksesAtAkses():
  try:
    id_role = request.form.get('id_role')
    page = request.form.get('page')

    filter_role = []
    filter_role.append(MAKSES.id_role==id_role,) if request.form.get('id_role') else filter.append([])
    
    filter_pek = []
    filter_pek.append(MPAGES.page==page,) if request.form.get('page') else filter.append([])
    
    qexists = db.session.query(MAKSES).with_entities(MAKSES.id).filter(MAKSES.status_aktif==1, MPAGES.id==MAKSES.id_page, *filter_role).scalar_subquery()
    qpages = db.session.query(MPAGES).with_entities(MPAGES.id, MPAGES.page, MPAGES.crud)\
                                      .filter(MPAGES.status_aktif==1,
                                              *filter_pek,
                                              ~func.exists(qexists)
                                              )\
                                      .all()
    data = []
    for row in qpages:
      data.append(row._asdict())
    message = 'Pages retrieved successfully' if qpages else 'Pages not found' 
    return jsonify({'status':'success', 'message':message, 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

def dropdownBagian():
  try:
    id = request.form.get('id_bagian')
    bagian = request.form.get('bagian')
    keterangan = request.form.get('keterangan')

    filter = []
    filter.append(MBAGIAN.id==id,) if request.form.get('id_bagian') else []
    filter.append(MBAGIAN.bagian==bagian,) if request.form.get('bagian') else []
    filter.append(MBAGIAN.keterangan==keterangan,) if request.form.get('keterangan') else []
    qbag = db.session.query(MBAGIAN).with_entities(MBAGIAN.id, MBAGIAN.bagian, MBAGIAN.keterangan, )\
                                      .filter(MBAGIAN.status_aktif==1,
                                              *filter,
                                              ).order_by(MBAGIAN.bagian,).all()
    data = []
    for row in qbag:
      data.append(row._asdict())
    message = 'Bagian retrieved successfully' if qbag else 'Bagian not found' 
    return jsonify({'status':'success', 'message':message, 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})
  
def dropdownEmployees():
  try:
    id_code = request.form.get('id_code')
    nik = request.form.get('nik')

    filter = []
    filter.append(MPLOY.id==id,) if request.form.get('id_code') else []
    filter.append(MPLOY.nik==nik,) if request.form.get('nik') else []
    
    qploy = db.session.query(MPLOY).with_entities(MPLOY.id, MPLOY.id_code, MPLOY.nik, MPLOY.nama, MPLOY.bagian, MPLOY.departement, 
                                                 MPLOY.jabatan, MPLOY.golongan, MPLOY.created_date, MPLOY.status_aktif, )\
                                      .filter(MPLOY.status_aktif==1,
                                              *filter,
                                              ).order_by(MPLOY.nik,).all()
    data = []
    for row in qploy:
      data.append(row._asdict())
    message = 'Data Employee retrieved successfully' if qploy else 'Employee not found' 
    return jsonify({'status':'success', 'message':message, 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})


''' GET GET AN '''



''' Master Bagian '''
def getMasterBagianDatatable():
  datatable = controller_module.Datatable(request.form)
  search_value = datatable.get_search_value()
  order = []
 
  sort_col_name = ['id', 'bagian', 'keterangan']
  sort_obj = {
    'id': MBAGIAN.id,
    'bagian': MBAGIAN.bagian,
    'keterangan': MBAGIAN.keterangan,
  }
  order = datatable.get_order(sort_col_name=sort_col_name, sort_obj=sort_obj)
  order.append(MBAGIAN.id.asc())

  jumlah_data_full = db.session.query(MBAGIAN).filter(MBAGIAN.status_aktif=='1').count()

  query_filtered = db.session.query(MBAGIAN).with_entities(MBAGIAN.id, MBAGIAN.bagian, MBAGIAN.keterangan,)\
                                          .filter(MBAGIAN.status_aktif=='1',
                                                  or_(MBAGIAN.id.like(search_value),
                                                      MBAGIAN.bagian.like(search_value),
                                                      MBAGIAN.keterangan.like(search_value),))\
                                          .order_by(*order)

  data_json = datatable.get_data_json_with_entities(query_filtered) 
  response = datatable.get_response(jumlah_data_full=jumlah_data_full, data_json=data_json)
  return jsonify(response)

@controller_akses.cek_akses_api('MASTER BAGIAN-R')
def getMasterBagian():
  try:
    id = request.args.get('id')
    bagian = request.args.get('bagian')
    keterangan = request.args.get('keterangan')
    filter = []
    filter.append(MBAGIAN.id==id) if id else []
    filter.append(MBAGIAN.bagian.like(f"%{bagian}%")) if bagian else []
    filter.append(MBAGIAN.keterangan.like(f"%{keterangan}%")) if keterangan else []

    qmploy = db.session.query(MBAGIAN).with_entities(MBAGIAN.id, MBAGIAN.bagian, MBAGIAN.keterangan,).filter(MBAGIAN.status_aktif==1, *filter,).all()

    data = []
    for row in qmploy:
      data.append(row._asdict())
    message = 'Bagian retrieved successfully' if qmploy else 'Bagian not found' 
    return jsonify({'status':'success', 'message':message, 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

@controller_akses.cek_akses_api('MASTER BAGIAN-C')
def addMasterBagian():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_input = {'created_by' : created_by}
    for row in data:
      data_input[row] = data.get(row)
      
    qcek = db.session.query(MBAGIAN).filter(MBAGIAN.status_aktif=='1', MBAGIAN.bagian==data_input['bagian'],).first()     
    if qcek:
      return jsonify({'status':'error', 'message':'Bagian is already exists'})
    
    add = MBAGIAN(**data_input)
    db.session.add(add)
    db.session.commit()

    data = add.to_dict()
    db.session.close()
    return jsonify({'status':'success', 'message':'Bagian added successfully', 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

@controller_akses.cek_akses_api('MASTER BAGIAN-U')
def editMasterBagian():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_edit = {'created_by' : created_by, 'created_date' : datetime.now(), }    
    for row in data:
      data_edit[row] = data.get(row)

    qcek = db.session.query(MBAGIAN).filter(MBAGIAN.bagian==data_edit['bagian'], MBAGIAN.status_aktif == 1).first()
    if qcek:
      if qcek.id != data_edit['id']:
        return jsonify({'status':'error', 'message':f"Bagian already exists"})

    qedit = db.session.query(MBAGIAN).filter(MBAGIAN.id==data_edit['id'], MBAGIAN.status_aktif == 1).first()
    if not qedit:
      return jsonify({'status':'error', 'message':'ID Bagian not found'})
    data_old = qedit.__dict__

    del data_old['_sa_instance_state']
    del data_old['id']
    data_old['id_history'] = data_edit['id']
    
    db.session.add(MBAGIANHIST(**data_old))
    db.session.commit()
    
    db.session.query(MBAGIAN).filter(MBAGIAN.id==data_edit['id']).update(data_edit)
    db.session.commit()
    db.session.close()
    return jsonify({'status':'success', 'message':'Kategori updated successfully', 'data':data_edit})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

@controller_akses.cek_akses_api('MASTER BAGIAN-D')
def deleteMasterBagian():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_delete = {'created_by' : created_by, 'created_date' : datetime.now(), 'status_aktif':0}
    for row in data:
      data_delete[row] = data.get(row)
    id_ = data_delete['id']
    qdel = db.session.query(MBAGIAN).filter(MBAGIAN.id==id_, MBAGIAN.status_aktif == 1).first()
    if not qdel:
      return jsonify({'status':'error', 'message':'ID Kategori not found'})
    data_old = qdel.__dict__

    del data_old['_sa_instance_state']
    del data_old['id']
    data_old['id_history'] = id_

    data_last = data_old.copy()
    data_last.update({
      'created_date': datetime.now(),
      'status_aktif': 0,
      'created_by': created_by
    })
    db.session.add(MBAGIANHIST(**data_old))
    db.session.commit()

    db.session.add(MBAGIANHIST(**data_last))
    db.session.commit()

    db.session.query(MBAGIAN).filter(MBAGIAN.id == id_, MBAGIAN.status_aktif == 1).delete(synchronize_session=False)
    db.session.commit()
    
    db.session.close()
    return jsonify({'status':'success', 'message':'Kategori deleted successfully', 'data':data_old})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})
  


''' Master Employees '''
def getEmployeesDatatable():
  datatable = controller_module.Datatable(request.form)
  search_value = datatable.get_search_value()
  order = []
 
  sort_col_name = ['id', 'nik', 'nama', ]
  sort_obj = {
    'id': MPLOY.id,
    'nik': MPLOY.nik,
    'nama': MPLOY.nama,
  }
  order = datatable.get_order(sort_col_name=sort_col_name, sort_obj=sort_obj)
  order.append(MPLOY.id)

  jumlah_data_full = db.session.query(MPLOY).filter(MPLOY.status_aktif=='1').count()

  query_filtered = db.session.query(MPLOY).with_entities(MPLOY.id,
                                                          MPLOY.nik,
                                                          MPLOY.nama)\
                                          .filter(MPLOY.status_aktif=='1',
                                                  or_(MPLOY.id.like(search_value),
                                                      MPLOY.nik.like(search_value),
                                                      MPLOY.nama.like(search_value)))\
                                          .order_by(*order)

  data_json = datatable.get_data_json_with_entities(query_filtered) 
  response = datatable.get_response(jumlah_data_full=jumlah_data_full, data_json=data_json)
  return jsonify(response)
