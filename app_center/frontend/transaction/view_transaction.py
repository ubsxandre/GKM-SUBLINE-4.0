from flask.helpers import flash
from app_center.frontend.transaction import fe_transaction_init
from app_center.authentication.akses import controller_akses
from flask import render_template, redirect, url_for, request, abort
from flask_login import login_user, login_required, current_user, logout_user

''' TRANSACTION OVEN SIKLUS'''
# @fe_transaction_init.route('/t-oven-siklus')
# @login_required
# @controller_akses.cek_page('TRANSACTION OVEN SIKLUS')
# @controller_akses.page_counter('t-oven-siklus')
# def t_oven_siklus():
#   """ Routing Transaction Oven Siklus"""
#   return render_template('transaction/oven_siklus/t-oven-siklus.html', page="t-oven-siklus")