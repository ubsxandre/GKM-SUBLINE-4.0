from flask.helpers import flash
from app_center.backend.master import model_master
from app_center.authentication.login import model
from flask import render_template, redirect, url_for, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app_center import db
from flask_login import login_user, login_required, current_user, logout_user
from app_center.authentication.akses import controller_akses
from app_center.api import controller_api
from sqlalchemy import func, case, and_, or_, cast, DATE, INT, literal_column, union_all, inspect
from sqlalchemy.orm import aliased, Session
from datetime import datetime, timedelta, time
from app_center.modules import controller_module
from app_center.backend.transaction.lembur import model_lembur
import json, os, pandas as pd, numpy as np


''' INIT TABLE MASTER '''
MABS = model_master.MasterEmployees
MABSHIST = model_master.MasterEmployeesHistory

''' INIT TABLE TRANSAKSI '''
TEL = model_lembur.TransLembur
TELHIST = model_lembur.TransLemburHistory


def getTransLemburDatatable():
  datatable = controller_module.Datatable(request.form)
  search_value = datatable.get_search_value()
  order = []
 
  sort_col_name = ['id', 'nik', 'nama', 'tgl_in', 'tgl_out', 'lokasi']
  sort_obj = {
    'id': TEL.id,
    'nik': TEL.nik,
    'nama': TEL.nama,
    'tgl_in': TEL.start_lembur,
    'tgl_out': TEL.end_lembur,
    'lokasi': TEL.lokasi,
  }
  order = datatable.get_order(sort_col_name=sort_col_name, sort_obj=sort_obj)
  order.append(TEL.id)

  jumlah_data_full = db.session.query(TEL).filter(TEL.status_aktif=='1').count()

  query_filtered = db.session.query(TEL).with_entities(TEL.id,
                                                        TEL.nik,
                                                          TEL.nama,
                                                          func.date_format(TEL.start_lembur, "%Y-%m-%d %H:%i:%s").label('start_lembur'),
                                                          func.date_format(TEL.end_lembur, "%Y-%m-%d %H:%i:%s").label('end_lembur'),
                                                          TEL.lokasi,)\
                                          .filter(TEL.status_aktif=='1',
                                                  or_(TEL.id.like(search_value),
                                                      TEL.nik.like(search_value),
                                                      TEL.nama.like(search_value),
                                                      TEL.start_lembur.like(search_value),
                                                      TEL.end_lembur.like(search_value),
                                                      TEL.lokasi.like(search_value)))\
                                          .order_by(*order)
  print(query_filtered.all())
  data_json = datatable.get_data_json_with_entities(query_filtered) 
  response = datatable.get_response(jumlah_data_full=jumlah_data_full, data_json=data_json)
  return jsonify(response)

def addTransLembur():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_input = {'created_by' : created_by}
    for row in data:
      data_input[row] = data.get(row)
    print(data_input)
    qcek1 = db.session.query(TEL).filter(TEL.status_aktif=='1', TEL.nik==data_input['nik'],
                                         or_(func.date_format(TEL.start_lembur, "%Y-%m-%d %H:%i").between(data_input['start_lembur'], data_input['end_lembur']) , 
                                             func.date_format(TEL.end_lembur, "%Y-%m-%d %H:%i").between(data_input['start_lembur'], data_input['end_lembur']) , 
                                             ),
                                        ).first()     
    if qcek1:
      return jsonify({'status':'error', 'message':'Hanya bisa lembur sekali dalam sehari'})
    
    # Kasih proteksi nggo ngecek diluar jam kerja. Kalau di dalam jam kerja ga bisa add.
    add = TEL(**data_input)
    db.session.add(add)
    db.session.commit()

    data = add.to_dict()
    db.session.close()
    return jsonify({'status':'success', 'message':'Lembur added successfully', 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

def editTransLembur():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_edit = {'created_by' : created_by, 'created_date' : datetime.now(), }    
    for row in data:
      data_edit[row] = data.get(row)
    qcek1 = db.session.query(TEL).filter(TEL.id==data_edit['id'], TEL.status_aktif == 1).first()
    if not qcek1:
      return jsonify({'status':'error', 'message':'ID Lembur not found'})

    qcek2 = db.session.query(TEL).filter(TEL.nik==data_edit['nik'], 
                                          or_(func.date_format(TEL.start_lembur, "%Y-%m-%d %H:%i").between(data_edit['start_lembur'], data_edit['end_lembur']) , 
                                             func.date_format(TEL.end_lembur, "%Y-%m-%d %H:%i").between(data_edit['start_lembur'], data_edit['end_lembur']) , 
                                             ),
                                          TEL.id!=data_edit['id'],
                                          TEL.status_aktif == 1).first()
    if qcek2:
      return jsonify({'status':'error', 'message':'Jam lembur tertimpa'})

    qedit = qcek1
    data_old = qedit.__dict__

    # Ini juga ditambahkan, tidak boleh nimpa jam kerja
    del data_old['_sa_instance_state']
    del data_old['id']
    data_old['id_history'] = data_edit['id']
    
    db.session.add(TELHIST(**data_old))
    db.session.commit()
    
    db.session.query(TEL).filter(TEL.id==data_edit['id']).update(data_edit)
    db.session.commit()
    db.session.close()
    return jsonify({'status':'success', 'message':'Lembur updated successfully', 'data':data_edit})
    return 'asd'
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})

def deleteTransLembur():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_delete = {'created_by' : created_by, 'created_date' : datetime.now(), 'status_aktif':0}
    for row in data:
      data_delete[row] = data.get(row)
    id_ = data_delete['id']
    print('PUKON', data_delete)

    qdel = db.session.query(TEL).filter(TEL.id==id_, TEL.status_aktif == 1).first()
    if not qdel:
      return jsonify({'status':'error', 'message':'ID Lembur not found'})
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
    db.session.add(TELHIST(**data_old))
    db.session.commit()

    db.session.add(TELHIST(**data_last))
    db.session.commit()

    db.session.query(TEL).filter(TEL.id == id_, TEL.status_aktif == 1).delete(synchronize_session=False)
    db.session.commit()
    
    db.session.close()
    return jsonify({'status':'success', 'message':'Kategori deleted successfully', 'data':data_old})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})