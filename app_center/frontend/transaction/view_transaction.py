from flask.helpers import flash
from app_center.frontend.transaction import fe_transaction_init
from app_center.authentication.akses import controller_akses
from flask import render_template, redirect, url_for, request, abort
from flask_login import login_user, login_required, current_user, logout_user

''' TRANSACTION ABSENSI'''
@fe_transaction_init.route('/t-absensi')
@login_required
@controller_akses.cek_page('TRANSACTION ABESNSI')
@controller_akses.page_counter('t-absensi')
def t_absensi():
  """ Routing Transaction Absensi"""
  return render_template('transaction/t-absensi.html', page="t-absensi")

''' TRANSACTION LEMBUR'''
@fe_transaction_init.route('/t-lembur')
@login_required
@controller_akses.cek_page('TRANSACTION LEMBUR')
@controller_akses.page_counter('t-lembur')
def t_lembur():
  """ Routing Transaction Lembur"""
  return render_template('transaction/t-lembur.html', page="t-lembur")




''' TRANSACTION OVEN SIKLUS'''
# @fe_transaction_init.route('/t-oven-siklus')
# @login_required
# @controller_akses.cek_page('TRANSACTION OVEN SIKLUS')
# @controller_akses.page_counter('t-oven-siklus')
# def t_oven_siklus():
#   """ Routing Transaction Oven Siklus"""
#   return render_template('transaction/oven_siklus/t-oven-siklus.html', page="t-oven-siklus")