# from flask_login import current_user
# from app_center.authentication.notifikasi import app_notifikasi, model_notifikasi
# from app_center.authentication.login import model
# from flask import render_template
# from app_center import db
# from datetime import datetime
# import sqlalchemy

# def lastUpdateNotifikasi(create_date):
#     last_update = datetime.strptime(str(create_date), '%Y-%m-%d %H:%M:%S') if create_date else None
#     time_now = datetime.strptime(str(datetime.now()).split('.')[0], '%Y-%m-%d %H:%M:%S')
#     time_delta = int((time_now-last_update).total_seconds()) if last_update else None
#     message = ''
#     if time_delta is None:
#       message = f"No Notification"
#     elif time_delta < 60:
#       message = f"{int(time_delta)} sec Ago"
#     elif 3600 > time_delta > 60:
#       message = f"{int(time_delta/60)} min Ago"
#     elif 3600*24 > time_delta > 3600:
#       message = f"{int(time_delta/(60*60))} hour Ago"
#     elif time_delta > 3600*24:
#       message = f"{int(time_delta/(60*60*24))} day Ago"
#     return message

# def notifikasi(nik):
#   data = model_notifikasi.m_notifikasi.query.filter_by(nik=nik).order_by(model_notifikasi.m_notifikasi.id.desc(), model_notifikasi.m_notifikasi.created_date.desc()).all()
#   for row in data:
#     row.time_message = lastUpdateNotifikasi(row.created_date)
#     row.date = row.created_date.date()
#   db.session.close()
#   return data

# def fetchNotifikasiUser(nik):
#   data = model_notifikasi.m_notifikasi.query.filter_by(nik=nik).order_by(model_notifikasi.m_notifikasi.id.desc(), model_notifikasi.m_notifikasi.created_date.desc()).limit(8).all()
#   for row in data:
#     row.time_message = lastUpdateNotifikasi(row.created_date)
#   db.session.close()
#   return data

# def bacaNotifikasi(id,nik):
#   data = model_notifikasi.m_notifikasi.query.filter_by(id=id,nik=nik).first()
#   if data is None:
#     return render_template('home/403.html')
#   else:
#     data.status_dibaca = 1
#     data.tanggal_baca = datetime.now()
#     db.session.commit()
#     db.session.close()

# def prosesNotifikasiAndon(nomor_mesin, kondisi):
#   ################################################################################################################
# # TABEL LOGIC
# # rantai jatuh  # kawat habis # rpm  # info  #  keterangan
# #   0           #       0     #  0   #  000  #   mesin aman
# #   0           #       0     #  1   #  003  #   rpm berhenti
# #   0           #       1     #  0   #  020  #   kawat habis
# #   0           #       1     #  1   #  023  #   kawat habis, rpm berhenti
# #   1           #       0     #  0   #  100  #   rantai jatuh
# #   1           #       0     #  1   #  103  #   rantai jatuh, rpm berhenti
# #   1           #       1     #  0   #  120  #   rantai jatuh, kawat habis
# #   1           #       1     #  1   #  123  #   rantai jatuh, kawat habis, rpm berhenti
# #################################################################################################################
#   logicObj = {
#     '000': 'Mesin Kembali Normal',
#     '001': 'RPM Berhenti',
#     '010': 'Kawat Habis',
#     '011': 'Kawat Habis dan RPM Berhenti',
#     '100': 'Rantai Jatuh',
#     '101': 'Rantai Jatuh dan RPM Berhenti',
#     '110': 'Rantai Jatuh dan Kawat Habis',
#     '111': 'Rantai Jatuh, Kawat Habis, Dan RPM Berhenti',
#   }


#   message = logicObj[kondisi]
#   route = 'dashboard-andon-gol5'
#   kategori = 'ANDON'
#   title = nomor_mesin
#   status_andon = 'NORMAL' if kondisi == '000' else 'MERAH'

#   model_notif = model_notifikasi.m_notifikasi
#   cache_notif = model_notifikasi.cache_notifikasi_andon
#   cek_andon = db.session.query(cache_notif.status).filter(cache_notif.nomor_mesin==nomor_mesin).first()
#   mengecek = None if cek_andon == None else cek_andon.status
#   db.session.close()

#   if status_andon != mengecek:
#     if mengecek == None:
#       add_cache = cache_notif(nomor_mesin=nomor_mesin, status=status_andon)
#       db.session.add(add_cache)
#       db.session.commit()
#       if status_andon == 'MERAH':
#         nik = db.session.query(model.User.nik).filter(sqlalchemy.or_(model.User.golongan=='5',model.User.golongan==5)).all()
#         recipient_gol_5 = [x.nik for x in nik]
#         print(recipient_gol_5)
#         for nik in recipient_gol_5:
#           add = model_notif(nik=nik,
#                             message=message,
#                             route=route,
#                             kategori=kategori,
#                             created_date=datetime.now(),
#                             title=title,
#                             status_andon = status_andon)
#           db.session.add(add)
#           db.session.commit()
#           db.session.close()
#     else:
#       cek_andon = db.session.query(cache_notif).filter(cache_notif.nomor_mesin==nomor_mesin).first()
#       cek_andon.status = status_andon
      
#       print(cek_andon.status)
#       print(status_andon)
#       db.session.commit()
#       nik = db.session.query(model.User.nik).filter(sqlalchemy.or_(model.User.golongan=='5',model.User.golongan==5)).all()
#       recipient_gol_5 = [x.nik for x in nik]
#       print(recipient_gol_5)
#       for nik in recipient_gol_5:
#         add = model_notif(nik=nik,
#                           message=message,
#                           route=route,
#                           kategori=kategori,
#                           created_date=datetime.now(),
#                           title=title,
#                           status_andon = status_andon)
#         db.session.add(add)
#         db.session.commit()
#         db.session.close()