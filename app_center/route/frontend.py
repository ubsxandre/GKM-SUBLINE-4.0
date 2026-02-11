def register_frontend(app):
  ''' LOGIN '''
  from app_center.frontend.login import fe_login_init as login
  app.register_blueprint(login)

  ''' DASHBOARD '''
  from app_center.frontend.dashboard import fe_dashboard_init as dashboard
  app.register_blueprint(dashboard)

  ''' MASTER '''
  from app_center.frontend.master import fe_master_init as master
  app.register_blueprint(master)

  ''' REPORT '''
  from app_center.frontend.report import fe_report_init as report
  app.register_blueprint(report)

  ''' TESTING '''
  from app_center.frontend.testing import fe_testing_init as testing  
  app.register_blueprint(testing)


  ''' ENSIKLOPEDIA '''
  from app_center.frontend.ensiklopedia import fe_ensiklopedia_init as ensiklopedia
  app.register_blueprint(ensiklopedia)
  

  ''' TRANSACTION '''
  from app_center.frontend.transaction import fe_transaction_init as transaction
  app.register_blueprint(transaction)