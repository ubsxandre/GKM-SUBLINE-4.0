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
from app_center.backend.transaction.absensi import model_absensi
import json, os, pandas as pd, numpy as np


''' INIT TABLE MASTER '''
MABS = model_master.MasterEmployees
MABSHIST = model_master.MasterEmployeesHistory

''' INIT TABLE TRANSAKSI '''
TABS = model_absensi.TransAbsensi
TABSHIST = model_absensi.TransAbsensiHistory
TIZINKELMAS = model_absensi.TransIzinKeluarMasuk
TIZINKELMASHIST = model_absensi.TransIzinKeluarMasukHistory



## Absensi didapat dari API IT, tidak perlu di simpan di database 4.0
## Hanya Read data tok

def getTransAbsensiDatatable():
  datatable = controller_module.Datatable(request.form)
  search_value = datatable.get_search_value()
  order = []
 
  sort_col_name = ['id', 'nik', 'nama', 'tgl_in', 'tgl_out', 'store']
  sort_obj = {
    'id': TABS.id,
    'nik': TABS.nik,
    'nama': TABS.nama,
    'tgl_in': TABS.tgl_in,
    'tgl_out': TABS.tgl_out,
    'store': TABS.store,
  }
  order = datatable.get_order(sort_col_name=sort_col_name, sort_obj=sort_obj)
  order.append(TABS.id)

  jumlah_data_full = db.session.query(TABS).filter(TABS.status_aktif=='1').count()

  query_filtered = db.session.query(TABS).with_entities(TABS.id,
                                                        TABS.nik,
                                                          TABS.nama,
                                                          func.date_format(TABS.tgl_in, "%Y-%m-%d %H:%i:%s").label('tgl_in'),
                                                          func.date_format(TABS.tgl_out, "%Y-%m-%d %H:%i:%s").label('tgl_out'),
                                                          TABS.lokasi,)\
                                          .filter(TABS.status_aktif=='1',
                                                  or_(TABS.id.like(search_value),
                                                      TABS.nik.like(search_value),
                                                      TABS.nama.like(search_value),
                                                      TABS.tgl_in.like(search_value),
                                                      TABS.tgl_out.like(search_value),
                                                      TABS.lokasi.like(search_value)))\
                                          .order_by(*order)

  data_json = datatable.get_data_json_with_entities(query_filtered) 
  response = datatable.get_response(jumlah_data_full=jumlah_data_full, data_json=data_json)
  return jsonify(response)


## Izin nembeng disini saja.
## Ngambil dari API IT
## Hanya Read tok

def getTransIzinDatatable():
  datatable = controller_module.Datatable(request.form)
  search_value = datatable.get_search_value()
  order = []
 
  sort_col_name = ['id', 'nik', 'nama', 'tgl_in', 'tgl_out', 'lokasi']
  sort_obj = {
    'id': TABS.id,
    'nik': TABS.nik,
    'nama': TABS.nama,
    'tgl_in': TABS.tgl_in,
    'tgl_out': TABS.tgl_out,
    'lokasi': TABS.lokasi,
  }
  order = datatable.get_order(sort_col_name=sort_col_name, sort_obj=sort_obj)
  order.append(TABS.id)

  jumlah_data_full = db.session.query(TABS).filter(TABS.status_aktif=='1').count()

  query_filtered = db.session.query(TABS).with_entities(TABS.id,
                                                        TABS.nik,
                                                          TABS.nama,
                                                          func.date_format(TABS.tgl_in, "%Y-%m-%d %H:%i:%s").label('tgl_in'),
                                                          func.date_format(TABS.tgl_out, "%Y-%m-%d %H:%i:%s").label('tgl_out'),
                                                          TABS.lokasi,)\
                                          .filter(TABS.status_aktif=='1',
                                                  or_(TABS.id.like(search_value),
                                                      TABS.nik.like(search_value),
                                                      TABS.nama.like(search_value),
                                                      TABS.tgl_in.like(search_value),
                                                      TABS.tgl_out.like(search_value),
                                                      TABS.lokasi.like(search_value)))\
                                          .order_by(*order)

  data_json = datatable.get_data_json_with_entities(query_filtered) 
  response = datatable.get_response(jumlah_data_full=jumlah_data_full, data_json=data_json)
  return jsonify(response)


def getTxIzinKeluarMasukDatatable():
  datatable = controller_module.Datatable(request.form)
  search_value = datatable.get_search_value()
  order = []
 
  sort_col_name = ['id', 'nik', 'nama', 'tgl_out', 'tgl_in', 'store', 'keperluan']
  sort_obj = {
    'id': TIZINKELMAS.id,
    'nik': TIZINKELMAS.nik,
    'nama': TIZINKELMAS.nama,
    'tgl_out': TIZINKELMAS.tgl_out,
    'tgl_in': TIZINKELMAS.tgl_in,
    'store': TIZINKELMAS.store,
    'keperluan': TIZINKELMAS.keperluan,
  }
  order = datatable.get_order(sort_col_name=sort_col_name, sort_obj=sort_obj)
  order.append(TIZINKELMAS.id)

  jumlah_data_full = db.session.query(TIZINKELMAS).filter(TIZINKELMAS.status_aktif=='1').count()

  query_filtered = db.session.query(TIZINKELMAS).with_entities(TIZINKELMAS.id,
                                                                TIZINKELMAS.nik,
                                                                  TIZINKELMAS.nama,
                                                                  func.date_format(TIZINKELMAS.tgl_in, "%Y-%m-%d %H:%i:%s").label('tgl_in'),
                                                          func.date_format(TIZINKELMAS.tgl_out, "%Y-%m-%d %H:%i:%s").label('tgl_out'),
                                                          TIZINKELMAS.store,
                                                          TIZINKELMAS.keperluan)\
                                          .filter(TIZINKELMAS.status_aktif=='1',
                                                  or_(TIZINKELMAS.id.like(search_value),
                                                      TIZINKELMAS.nik.like(search_value),
                                                      TIZINKELMAS.nama.like(search_value),
                                                      TIZINKELMAS.tgl_in.like(search_value),
                                                      TIZINKELMAS.tgl_out.like(search_value),
                                                      TIZINKELMAS.store.like(search_value),
                                                      TIZINKELMAS.keperluan.like(search_value)))\
                                          .order_by(*order)

  data_json = datatable.get_data_json_with_entities(query_filtered) 
  response = datatable.get_response(jumlah_data_full=jumlah_data_full, data_json=data_json)
  return jsonify(response)


@controller_akses.cek_akses_api('T-IZIN-KELUAR-MASUK-R')
def getTxIzinKeluarMasuk():
  try:
    id = request.args.get('id')
    nik = request.args.get('nik')
    nama = request.args.get('nama')
    tgl_out = request.args.get('tgl_out')
    tgl_in = request.args.get('tgl_in')
    store = request.args.get('store')
    keperluan = request.args.get('keperluan')
    filter = []
    filter.append(TIZINKELMAS.id==id) if id else []
    filter.append(TIZINKELMAS.nik.like(f"%{nik}%")) if nik else []
    filter.append(TIZINKELMAS.nama.like(f"%{nama}%")) if nama else []
    filter.append(TIZINKELMAS.tgl_out.like(f"%{tgl_out}%")) if tgl_out else []
    filter.append(TIZINKELMAS.tgl_in.like(f"%{tgl_in}%")) if tgl_in else []
    filter.append(TIZINKELMAS.store.like(f"%{store}%")) if store else []
    filter.append(TIZINKELMAS.keperluan.like(f"%{keperluan}%")) if keperluan else []

    qmploy = db.session.query(TIZINKELMAS).with_entities(TIZINKELMAS.id, TIZINKELMAS.nik, TIZINKELMAS.nama, TIZINKELMAS.tgl_out, TIZINKELMAS.tgl_in, TIZINKELMAS.store, TIZINKELMAS.keperluan).filter(TIZINKELMAS.status_aktif==1, *filter,).all()

    data = []
    for row in qmploy:
      data.append(row._asdict())
    message = 'Bagian retrieved successfully' if qmploy else 'Bagian not found' 
    return jsonify({'status':'success', 'message':message, 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})


@controller_akses.cek_akses_api('T-IZIN-KELUAR-MASUK-C')
def addTxIzinKeluarMasuk():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_input = {'created_by' : created_by}
    for row in data:
      data_input[row] = data.get(row)
    today = datetime.now().strftime("%Y-%m-%d")
    today_time = datetime.now()

    qnik = db.session.query(MABS).filter(MABS.status_aktif=='1', MABS.id_code==data_input['keplek']).first()
    if not qnik:
      return jsonify({'status':'error', 'message':'Keplek not found'})
    
    print('Otomatis ', data_input)
    # Proteksi harus absen - API IT
    # Proteksi harus tidak izin kerja - API IT
    # PRoteksi harus tanggal keluar harus lebih kecil dari tanggal masuk
    qcek = db.session.query(TIZINKELMAS).filter(TIZINKELMAS.status_aktif=='1', TIZINKELMAS.nik==qnik.nik, func.date_format(TIZINKELMAS.tgl_out, '%Y-%m-%d') == today).order_by(TIZINKELMAS.tgl_out.desc()).first()     

    if data_input['action'] == 'keluar':
      if qcek:
        dcek = qcek.__dict__
        if dcek['tgl_in'] is None:
          return jsonify({'status':'error', 'message':'Tadi setelah keluar, belum checkin lagi'})

      add = TIZINKELMAS(**{'nik': qnik.nik, 'nama': qnik.nama, 'bagian': qnik.bagian, 'store': qnik.store, 'tgl_out': today_time, 'keperluan': data_input['keperluan'], 'created_by': created_by, 'created_date': datetime.now()})
      db.session.add(add)
      db.session.commit()

      data = add.to_dict()
      db.session.close()

    if data_input['action'] == 'masuk':
      if not qcek:
        return jsonify({'status':'error', 'message':'Tadi belum keluar, tidak usah checkin'})
      else:
        dcek = qcek.__dict__
        dcek_ = dcek['id']
        if dcek['tgl_in'] is None:
          qedit = db.session.query(TIZINKELMAS).filter(TIZINKELMAS.id==dcek_, TIZINKELMAS.status_aktif == 1).first()
          if not qedit:
            return jsonify({'status':'error', 'message':'ID Bagian not found'})
          data_old = qedit.__dict__

          del data_old['_sa_instance_state']
          del data_old['id']
          data_old['id_history'] = dcek_
          
          db.session.add(TIZINKELMASHIST(**data_old))
          db.session.commit()
          
          db.session.query(TIZINKELMAS).filter(TIZINKELMAS.id==dcek_).update({'tgl_in': today_time, 'created_by': created_by, 'created_date': datetime.now()})
          db.session.commit()
          db.session.close()
        else:
          return jsonify({'status':'error', 'message':'Tadi sudah checkin, tidak usah checkin lagi'})

    return jsonify({'status':'success', 'message':'Izin added successfully', 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})


@controller_akses.cek_akses_api('T-IZIN-KELUAR-MASUK-C')
def addTxIzinKeluarMasukManual():
  try:
    data = request.get_json()
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_input = {'created_by' : created_by}
    for row in data:
      data_input[row] = data.get(row)
    
    data = []
    qnik = db.session.query(MABS).filter(MABS.status_aktif=='1', MABS.id_code==data_input['keplek']).first()
    if not qnik:
      return jsonify({'status':'error', 'message':'Keplek not found'})
    
    # Proteksi harus absen
    # PRoteksi harus tanggal keluar harus lebih kecil dari tanggal masuk

    if data_input['tgl_out'] is not None and data_input['tgl_in'] is not None:
      tgl_out_dt = datetime.strptime(data_input['tgl_out'], '%Y-%m-%dT%H:%M')
      tgl_in_dt  = datetime.strptime(data_input['tgl_in'],  '%Y-%m-%dT%H:%M')
      qcek = db.session.query(TIZINKELMAS).filter(TIZINKELMAS.status_aktif == '1',
                                                  TIZINKELMAS.nik == qnik.nik,
                                                    or_(
                                                      TIZINKELMAS.tgl_out.between(tgl_out_dt, tgl_in_dt),
                                                      TIZINKELMAS.tgl_in.between(tgl_out_dt, tgl_in_dt)
                                                    )
                                                  ).first()
      if qcek:
        return jsonify({'status':'error', 'message':'NIK is already exists in the given time range'})
      add = TIZINKELMAS(**{'nik': qnik.nik, 'nama': qnik.nama, 'bagian': qnik.bagian, 'store': qnik.store, 'tgl_out': data_input['tgl_out'], 'tgl_in': data_input['tgl_in'], 'keperluan': data_input['keperluan'], 'created_by': created_by, 'created_date': datetime.now()})
      db.session.add(add)
      data = add.to_dict()
      db.session.commit()

    
    if data_input['tgl_out'] is not None and data_input['tgl_in'] is None:
      tgl_out_date = datetime.strptime(data_input['tgl_out'], '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d') if data_input.get('tgl_out') else None
      qcek = db.session.query(TIZINKELMAS).filter(TIZINKELMAS.status_aktif=='1', TIZINKELMAS.nik==qnik.nik, func.date_format(TIZINKELMAS.tgl_out, '%Y-%m-%d') == tgl_out_date).order_by(TIZINKELMAS.tgl_out.desc()).first()
      if qcek:
        dcek = qcek.__dict__
        if dcek['tgl_in'] is None:
          return jsonify({'status':'error', 'message':'Tadi setelah izin keluar, belum checkin lagi'})
      add = TIZINKELMAS(**{'nik': qnik.nik, 'nama': qnik.nama, 'bagian': qnik.bagian, 'tgl_out': data_input['tgl_out'], 'created_by': created_by, 'created_date': datetime.now()})
      db.session.add(add)
      data = add.to_dict()
      db.session.commit()

    if data_input['tgl_out'] is None and data_input['tgl_in'] is not None:
      tgl_in_date  = datetime.strptime(data_input['tgl_in'],  '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d') if data_input.get('tgl_in')  else None
      qcek = db.session.query(TIZINKELMAS).filter(TIZINKELMAS.status_aktif=='1', TIZINKELMAS.nik==qnik.nik, func.date_format(TIZINKELMAS.tgl_out, '%Y-%m-%d') == tgl_in_date).order_by(TIZINKELMAS.tgl_out.desc()).first()
      if not qcek:
        return jsonify({'status':'error', 'message':'Tidak ada izin keluar di tanggal ini, tudak usah checkin'})
      if qcek:
        dcek = qcek.__dict__
        dcek_ = dcek['id']
        if dcek['tgl_in'] is None:
          tgl_in_dt = datetime.strptime(data_input['tgl_in'], '%Y-%m-%dT%H:%M')
          if dcek['tgl_out'] > tgl_in_dt:
            return jsonify({'status':'error', 'message':'Tanggal masuk tidak boleh lebih kecil dari tanggal keluar'})
          data_old = qcek.__dict__

          del data_old['_sa_instance_state']
          del data_old['id']
          data_old['id_history'] = dcek_

          db.session.add(TIZINKELMASHIST(**data_old))
          db.session.commit()
          data = add.to_dict()
          
          db.session.query(TIZINKELMAS).filter(TIZINKELMAS.id==dcek_).update({'tgl_in': tgl_in_dt, 'created_by': created_by, 'created_date': datetime.now()})
          db.session.commit()
          db.session.close()
          
    db.session.close()
    return jsonify({'status':'success', 'message':'Izin added successfully', 'data':data})
  except Exception as e:
    print(e)
    return jsonify({'status':'error', 'message':str(e)})