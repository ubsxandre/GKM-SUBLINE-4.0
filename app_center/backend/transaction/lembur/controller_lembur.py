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
