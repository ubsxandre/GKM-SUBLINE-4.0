from flask.helpers import flash
from app_center.frontend.master import fe_master_init
from app_center.authentication.akses import controller_akses
from flask import render_template, redirect, url_for, request, abort
from flask_login import login_user, login_required, current_user, logout_user

''' MASTER ROLES '''
@fe_master_init.route('/m-roles')
@login_required
@controller_akses.cek_page('MASTER ROLES')
@controller_akses.page_counter('m-roles')
def m_roles():
  """ Routing Master Roles"""
  return render_template('master/user/m-roles.html', page="m-roles")

''' MASTER PAGES '''
@fe_master_init.route('/m-pages')
@login_required
@controller_akses.cek_page('MASTER PAGES')
@controller_akses.page_counter('m-pages')
def m_pages():
  """ Routing Master Pages"""
  return render_template('master/user/m-pages.html', page="m-pages")

''' MASTER ACCESS '''
@fe_master_init.route('/m-access')
@login_required
@controller_akses.cek_page('MASTER ACCESS')
@controller_akses.page_counter('m-access')
def m_access():
  """ Routing Master Access"""
  return render_template('master/user/m-access.html', page="m-access")

''' MASTER ACCESS MANAGEMENT '''
@fe_master_init.route('/access-management')
@login_required
@controller_akses.cek_page('ACCESS MANAGEMENT')
@controller_akses.page_counter('access-management')
def access_management():
  """ Routing Master Access Management """
  return render_template('access_management/access-management.html', page="access-management")


'''MASTER DEPARTEMEN'''
@fe_master_init.route('/m-departemen')
@login_required
@controller_akses.cek_page('MASTER DEPARTEMEN')
@controller_akses.page_counter('m-departemen')
def m_departemen():
  """ Routing Master Departemen """
  return render_template('master/m-departemen.html', page="m-departemen")


'''MASTER EMPLOYEES'''
@fe_master_init.route('/m-employees')
@login_required
@controller_akses.cek_page('MASTER EMPLOYEES')
@controller_akses.page_counter('m-employees')
def m_employees():
  """ Routing Master Employees """
  return render_template('master/user/m-employees.html', page="m-employees")