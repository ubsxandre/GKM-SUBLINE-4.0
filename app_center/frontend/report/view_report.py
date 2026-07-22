from flask.helpers import flash
from app_center.frontend.report import fe_report_init
from app_center.authentication.akses import controller_akses
from flask import render_template, redirect, url_for, request, abort
from flask_login import login_user, login_required, current_user, logout_user

''' REPORT IN OUT '''
@fe_report_init.route('/report-in-out')
@login_required
@controller_akses.cek_page('REPORT IN - OUT')
@controller_akses.page_counter('report-in-out')
def report_in_out():
  """ Routing REPORT In - Out """
  return render_template('report/report-in-out.html', page="report-in-out")
