from flask import render_template, redirect, url_for, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app_center import db, FILESDIR, reddb, REDIS_NAME, BASEDIR, ENSIKLOPEDIADIR
from flask_login import login_user, login_required, current_user, logout_user
from flask_minify import Minify, decorators as minify_decorators
from app_center.authentication.akses import controller_akses
from app_center.api import controller_api
from app_center.backend.ensiklopedia import model_ensiklopedia
from sqlalchemy import func, case, and_, or_, cast, DATE, INT, literal_column, union_all, exists
from datetime import datetime, timedelta
from app_center.authentication.login import model
import pandas as pd, io, base64, os, json
from werkzeug.utils import secure_filename
import locale
import copy

# locale.setlocale(locale.LC_TIME, 'id_ID')

def waktu_sekarang():
  return datetime.now()

''' INITIAL MODEL '''
ENSIK = model_ensiklopedia.Ensiklopedia
ENSIKHISTORY = model_ensiklopedia.EnsiklopediaHistory
USER = model.User

''' CONTROLLER ENSIKLOPEDIA '''
def addEnsiklopedia():
  try:
    data = json.loads(request.form.get('json'))
    files = request.files['file_ensiklopedia']
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    data_input = {'created_by': created_by}
    for row in data:
      data_input[row] = data.get(row)
    
    add =  ENSIK(**data_input)
    db.session.add(add)
    db.session.commit()
    id_ensiklopedia = add.id

    file_name = files.filename.split('.')[0]
    fileformat = files.filename.split('.')[-1]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = secure_filename(f"{timestamp}-{file_name}.{fileformat}")
    file_folder = os.path.join(ENSIKLOPEDIADIR, filename)
    files.save(file_folder)

    db.session.query(ENSIK).filter(ENSIK.id == id_ensiklopedia).update({'file_name': filename,
                                                                        'ekstension': fileformat,})
    db.session.commit()
    db.session.close()
    return jsonify({'status': 'success', 'data': data_input, 'message': 'Ensiklopedia berhasil ditambahkan'})
  except Exception as e:
    print(f"Error adding ensiklopedia: {e}")
    return jsonify({'status': 'error', 'message': str(e)}), 500

def getEnsiklopedia():
  try:
    data = db.session.query(ENSIK).filter(ENSIK.status_aktif == '1').all()
    result = []
    for row in data:
      user = db.session.query(USER).filter(USER.nik == row.created_by, USER.status_aktif=='1').first()
      pembuat = user.nama if user else row.created_by
          
      result.append({
        'id': row.id,
        'judul': row.judul,
        'file_name': row.file_name,
        'ekstension': row.ekstension,
        'ukuran_file': row.ukuran_file,
        'tipe': row.tipe,
        'pembuat': pembuat,
        'tanggal_pembuatan': row.created_date.strftime('%d-%B-%Y'),
      })
    
    db.session.close()
    return jsonify({'status': 'success', 'data': result})
  except Exception as e:
    print(f"Error getting ensiklopedia: {e}")
    return jsonify({'status': 'error', 'message': str(e)}), 500

def deleteEnsiklopedia():
  try:
    id_form = request.form.get('id_form')
    created_by = current_user.nik if current_user.is_authenticated else 'SYSTEM'
    qdelete = db.session.query(ENSIK).filter(ENSIK.id == id_form, ENSIK.status_aktif=='1').first()
    if not qdelete:
      return jsonify({'status': 'error', 'message': 'Ensiklopedia not found'}), 404
    data_old = qdelete.__dict__
    id_delete = data_old['id']
    
    del data_old['id']
    del data_old['_sa_instance_state']
    
    data_delete = copy.copy(data_old)
    data_delete['id_history'] = id_delete
    data_delete['keterangan'] = f"Dibuat oleh {data_old['created_by']} pada {data_old['created_date'].strftime('%d-%B-%Y %H:%M:%S')}"
    data_delete['status_aktif'] = 0
    data_delete['created_by'] = created_by
    data_delete['created_date'] = waktu_sekarang()

    delete = ENSIKHISTORY(**data_delete)
    db.session.add(delete)
    db.session.commit()

    db.session.query(ENSIK).filter(ENSIK.id==id_form, ENSIK.status_aktif == '1').delete()
    db.session.commit()

    data = delete.to_dict()
    db.session.close()
    return jsonify({'status': 'success', "message": 'Ensiklopedia deleted successfully', 'data': data})
  except Exception as e:
    print(f"Error deleting ensiklopedia: {e}")
    return jsonify({'status': 'error', 'message': str(e)}), 500