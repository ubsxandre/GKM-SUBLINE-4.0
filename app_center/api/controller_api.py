from sqlalchemy import func, true, and_, not_
from datetime import datetime as dt, timedelta, date
from flask import json, jsonify, request, flash, redirect, Response, send_file
import os, csv, io, pandas as pd, requests, numpy as np
import datetime
from app_center.modules import controller_module
from app_center.api import model_api
from flask_login import current_user
from app_center import db, BASEDIR
from app_center.authentication.logs import controller_logs


from sklearn.cluster import KMeans
# from scipy.stats import gaussian_kde, shapiro, normaltest
# from scipy.signal import find_peaks
from collections import Counter
# import hdbscan, os, re, math

'''' INITIAL MODEL '''
MCOK =  model_api.m_cookie_api

''' TOKEN API IT '''

def tokenAPI():
  payload    = {'authKey': 'm7hgShvLwdgwdyR4JndTtQFUeYfnYYsMmM9uQUHHtc9QvAFvcG58HqQPX96x5RcmQYkTEJbgNUc49FQmDauMg'}
  loginToken = "http://172.20.33.42/ubs-api/get_token"
  login = requests.post(loginToken, data=json.dumps(payload))
  token = json.loads(login.text)
  headers = {'Authorization': 'Bearer {}'.format(token['Authentication'])}
  return headers


''' TOKEN API HRIS '''

def getVerifToken():
  loginToken = f'http://172.20.140.35/HRIS.Web/Login'
  login = requests.Session()
  response = login.get(loginToken)
  verifToken = response.cookies.get_dict()['__RequestVerificationToken_L0hSSVMuV2Vi0']
  return verifToken

def getCookies():
  loginToken = f'http://172.20.140.35/HRIS.Web/Logon'
  header = getVerifToken()
  headers = { 'Content-type':'application/json', 
              '__RequestVerificationToken':''+header+''
            }
  params = {'rememberMe':'false'}
  id_pw_hris = '015019!@#intermilan'
  cipher = controller_module.AES128(key='8080808080808080', iv='8080808080808080', plaintext=id_pw_hris)
  params['cipher'] = cipher.encryptCBC()
  login = requests.post(loginToken, headers=headers, params=params)
  cookies = login.headers['Set-Cookie'].split('.AspNet.ApplicationCookie=')[1].split('; ')[0]
  return cookies

def getCookiePerDay():
  time = datetime.datetime.now()
  time = datetime.datetime.strftime(time, '%Y-%m-%d')
  findCookie = MCOK.query.filter(
    MCOK.status_aktif == 1,
    MCOK.created_date.like(time+'%')
  ).with_entities(
    MCOK.cookie
  ).first()
  
  if findCookie is None:
    cookie = getCookies()
    add = MCOK(
      cookie = cookie,
      created_date = datetime.datetime.now(),
      created_by = current_user.nik,
      status_aktif = 1
    )
    db.session.add(add)
    db.session.commit()
  else:
    cookie = findCookie[0]
  
  return cookie

def getSSO(nik, password):
  get_api_sso = None
  try:
    get_token_api = tokenAPI()
    api_sso = f"http://172.20.33.42/ubs-api/umum/Get_login?user={nik}&password={password}"
    get_api_sso  = requests.get(api_sso, headers=get_token_api)
    json_api_sso  = get_api_sso.json()
    return json_api_sso[0]['HASIL']
  except Exception as e: 
    if get_api_sso == None:
      return 'XZ'
    elif 'Password anda sudah Expired' in get_api_sso.text:
      return 'X'
    else:
      return 'Z'
    
''' LIST GET DATA API '''

def getDepartment():
  try:
    get_department = f'http://172.20.33.42/hcis/api/v1/organization/department?page=1&isHigherUpSearch=true&status=1'
    
    tokenCookie = getCookiePerDay()
    
    headers = { 'Content-type':'application/json', 
              'Accept':'application/json', 
              'Cookie':'.AspNet.ApplicationCookie='+tokenCookie
              }
    route = requests.get(get_department,headers=headers)
    data = route.json()
    return jsonify(data['listOrganization'])
  except Exception as e:
    print(e)
    return flash('Error to Get Data Department, Please Try Again')
  
def getEmployeeHCIS(nik):
  try:
    get_emp = f'http://172.20.33.42/hcis/api/v1/employee/getEmployeePosition?employeeId={nik}'
    tokenCookie = getCookiePerDay()
    headers = { 'Content-type':'application/json', 
              'Accept':'application/json', 
              'Cookie':'.AspNet.ApplicationCookie='+tokenCookie
              }
    route = requests.get(get_emp,headers=headers)
    data = route.json()
    return jsonify(data)
  except Exception as e:
    print(e)

def getSubDepartmentHCIS():
  try:
    get_sub_department = f'http://172.20.140.35/HRIS.Web/api/v1/organization/subdepartment?status=1'
    
    tokenCookie = getCookiePerDay()
    
    headers = { 'Content-type':'application/json', 
              'Accept':'application/json', 
              'Cookie':'.AspNet.ApplicationCookie='+tokenCookie
              }
    route = requests.get(get_sub_department,headers=headers)
    data = route.json()
    return jsonify(data['listOrganization'])
  except Exception as e:
    print(e)
    return []

def getHCISJabatan(search):
  try:
    url = f"http://172.20.33.42/hcis/api/v1/position/GetPositionInformation?query=&deptId={search}&subDeptId=&sectId=&subSectId=&isVacant=false&status=1"
    tokenCookie = getCookiePerDay()
    
    headers = { 'Content-type':'application/json', 
              'Accept':'application/json', 
              'Cookie':'.AspNet.ApplicationCookie='+tokenCookie
              }
    route = requests.get(url,headers=headers)
    data = route.json()
    return jsonify(data['PositionInformationList'])
  except Exception as e:
    print(e)
    return jsonify(e)
  
def getHCISKarAutoComplete(search):
  try:
    url = f"http://172.20.33.42/hcis/api/v1/employee/userswithpositions?name={search}"

    tokenCookie = getCookiePerDay()
    
    headers = { 'Content-type':'application/json', 
              'Accept':'application/json', 
              'Cookie':'.AspNet.ApplicationCookie='+tokenCookie
              }
    route = requests.get(url,headers=headers)
    data = route.json()
    return jsonify(data)
  except Exception as e:
    print(e)
    return None
  
def getAdmkar(nik):
  try:
    get_token_api = tokenAPI()
    get_admkar = f"http://172.20.33.42/ubs-api/admkar/Get_Data?nik={nik}&rfid=''"
    get_data_admkar = requests.get(get_admkar, headers=get_token_api)
    data = get_data_admkar.json()
    return data
  except Exception as e:
    print(e)
    return None


def getAbsensi(nik):
  try:
    get_token_api = tokenAPI()
    get_admkar = f"http://172.20.33.42/ubs-api/admkar/Get_Data?nik={nik}&rfid=''"
    get_data_admkar = requests.get(get_admkar, headers=get_token_api)
    data = get_data_admkar.json()
    return data
  except Exception as e:
    print(e)
    return None

def getIzin(nik):
  try:
    get_token_api = tokenAPI()
    get_admkar = f"http://172.20.33.42/ubs-api/admkar/Get_Data?nik={nik}&rfid=''"
    get_data_admkar = requests.get(get_admkar, headers=get_token_api)
    data = get_data_admkar.json()
    return data
  except Exception as e:
    print(e)
    return None


  