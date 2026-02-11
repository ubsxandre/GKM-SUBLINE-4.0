def register_backend(app):
  ''' LOGIN '''
  from app_center.authentication.login import app_login_init as login
  app.register_blueprint(login)

  ''' API EKSTERNAL '''
  from app_center.api import app_api as api
  app.register_blueprint(api)

  '''  LOGS '''
  from app_center.authentication.logs import app_logs as logs
  app.register_blueprint(logs)

  ''' NOTIFIKASI '''
  from app_center.authentication.notifikasi import app_notifikasi as notifikasi
  app.register_blueprint(notifikasi)

  ''' AKSES '''
  from app_center.authentication.akses import app_akses as akses
  app.register_blueprint(akses)

  ''' DASHBOARD '''
  from app_center.backend.dashboard import be_dashboard_init as dashboard
  app.register_blueprint(dashboard)

  ''' MASTER '''
  from app_center.backend.master import be_master_init as master
  app.register_blueprint(master)

  ''' TESTIING '''
  from app_center.backend.testing import be_testing_init as testing
  app.register_blueprint(testing)

  ''' WEBSOCKET '''
  from app_center.websocket import app_socket
  app.register_blueprint(app_socket)

  ''' ENSIKLOPEDIA '''
  from app_center.backend.ensiklopedia import be_ensiklopedia_init as ensiklopedia
  app.register_blueprint(ensiklopedia)
  
