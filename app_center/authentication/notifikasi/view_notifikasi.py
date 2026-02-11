# from app_center.authentication.notifikasi import app_notifikasi, controller_notifikasi, model_notifikasi
# from flask import render_template
# from flask_login import login_required, current_user

# # Routing Notifikasi
# @app_notifikasi.route('/notifikasi-<nik>')
# @login_required
# def notifikasi(nik):
#   return 'kampas kopling'
#   # if nik != current_user.nik:
#   #   return render_template('home/403.html')
#   # else:
#   #   controller_document.setUserVariable()
#   #   data = controller_notifikasi.notifikasi(nik)
#   #   return render_template('notifikasi/notifikasi.html', data=data)

# @app_notifikasi.route('/fetch-notifikasi-user-<nik>',  methods=['GET', 'POST'])
# @login_required
# def fetch_notifikasi_user(nik):
#   if nik != current_user.nik:
#     return render_template('home/403.html')
#   else:
#     data = controller_notifikasi.fetchNotifikasiUser(nik)
#     print(data)
#     return render_template('accounts/notifikasi-dropdown.html', data=data)

# @app_notifikasi.route('/baca-notifikasi-<id>-<nik>', methods=['GET', 'POST'])
# @login_required
# def baca_notifikasi(id,nik):
#   if nik != current_user.nik:
#     return render_template('home/403.html')
#   else:
#     controller_notifikasi.bacaNotifikasi(id,nik)
#     return 'Hayo Mau Ngapain Kamu'