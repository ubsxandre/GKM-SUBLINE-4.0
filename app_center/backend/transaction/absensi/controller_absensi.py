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


def getTransAbsensiDatatable():
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
