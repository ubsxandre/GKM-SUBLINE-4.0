from flask import Flask, url_for, render_template, session, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, case, and_, or_, cast, DATE, INT, literal_column, union_all
from flask_migrate import Migrate
from config import DevelopmentConfig
from flask_login import LoginManager, current_user
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from pytz import timezone
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from flask_swagger_ui import get_swaggerui_blueprint
import MySQLdb.cursors, os, influxdb_client
# import influxdb_client, os, time
from flask_socketio import SocketIO


''' ENVIRONMENT DATABASE, FOLDER FILE, LOGS '''
HOST = str(os.environ.get("DB_HOST"))
DATABASE = str(os.environ.get("DB_DATABASE"))
USERNAME = str(os.environ.get("DB_USERNAME"))
PASSWORD = str(os.environ.get("DB_PASSWORD"))
DATABASE_FILE = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}'
BASEDIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ERRORLOGDIR = os.path.join(BASEDIR,'./static/logs') 
FILESDIR = os.path.join(BASEDIR, "./static/files")
AUTH_KEY = os.environ.get('SECRET_KEY')
SAVED_AUTH_TOKEN = {}
SAVED_HASHED_NIK = {}
SWAGGER_URL = '/swagger'
API_URL = "../static/swagger/!swagger-main.json"
REDIS_NAME = os.environ.get('COOKIE')
ENSIKLOPEDIADIR = os.path.join(BASEDIR, './static/files/ensiklopedia')
                                
''' IMPORT EXTENSIONS INSTANCE '''
reddb = None
if os.environ.get('FLASK_RUN_HOST') == '172.20.140.98':
  import redis
  reddb = redis.Redis(host='172.20.140.98', port=6379, decode_responses=True)
## Development. Download reddis dulu di windows
# else:
#   import redis
#   reddb = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
db = SQLAlchemy()
migrate = Migrate()
mysql = MySQL()
curMysql = MySQLdb.cursors.DictCursor
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
# scheduler = BackgroundScheduler(timezone=timezone('Asia/Jakarta'),
#                                 jobstores={'default':SQLAlchemyJobStore(url=DATABASE_FILE, tablename='apscheduler_jobs')})

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)

token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
url = os.environ.get("INFLUXDB_URL")
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org, timeout=120000)

# token_wit = os.environ.get("INFLUXDB_TOKEN_WIT")
# username_wit = os.environ.get("INFLUXDB_USERNAME_WIT")
# password_wit = os.environ.get("INFLUXDB_PASSWORD_WIT")
# org_wit = os.environ.get("INFLUXDB_ORG_WIT")
# url_wit = os.environ.get("INFLUXDB_URL_WIT")
# # client_wit = influxdb_client.InfluxDBClient(url=url_wit, username=username_wit, password=password_wit, org=org_wit, ssl=True, verify_ssl=True, timeout=600000)
# client_wit = influxdb_client.InfluxDBClient(url=url_wit, token=token_wit, org=org_wit, timeout=600000)

def center_app(config=DevelopmentConfig): 
    
  ''' INITIALIZE HANDLING ERRORS '''
  from app_center.errors import handlers 

  app.config.from_object(config)
  app.config["DEBUG"] = True   
  # CORS(app) # Mengaktifkan CORS untuk seluruh aplikasi
  # CORS(app, resources={r"/api/*": {"origins": "http://frontend.com"}})

  ''' SET THE DURATION FOR THE "REMEMBER ME" COOKIE '''
  # app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)  
  # app.config['REMEMBER_COOKIE_SECURE'] = True
  # app.config['SESSION_COOKIE_SECURE'] = True
  # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=5)

  @app.after_request
  def after_request(response):
    if os.environ.get('FLASK_RUN_HOST') == '172.20.140.98':
      response.headers["Cache-Control"] = "public, max-age=86400"
      return response
    else:
      response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
      response.headers["Expires"] = 0
      response.headers["Pragma"] = "no-cache"
      return response
    
  from app_center.modules import controller_module as cmod
  @app.before_request
  def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=45)
    session.modified = True
    if current_user.is_authenticated == True:
      bearer_app = None
      if os.environ.get('FLASK_RUN_HOST') == '172.20.140.98':
        reddb.get(f"{REDIS_NAME}-{current_user.nik}-{datetime.now().strftime('%d-%m-%Y')}") 
      elif f"{REDIS_NAME}-{current_user.nik}-{datetime.now().strftime('%d-%m-%Y')}" in SAVED_AUTH_TOKEN:
        SAVED_AUTH_TOKEN[f"{REDIS_NAME}-{current_user.nik}-{datetime.now().strftime('%d-%m-%Y')}"]
      if current_user.bearer_token != bearer_app:
        current_user.bearer_token = cmod.generateBearerToken(current_user.nik)
    g.user = current_user
      
  app.config['MYSQL_HOST']=os.environ.get('DB_HOST')
  app.config['MYSQL_USER']=os.environ.get('DB_USERNAME')
  app.config['MYSQL_PASSWORD']=os.environ.get('DB_PASSWORD')
  app.config['MYSQL_DB']=os.environ.get('DB_DATABASE')
  app.config['SESSION_COOKIE_NAME'] = os.environ.get('COOKIE')

  ''' INITIALIZE EXTENSION INSTANCES '''
  mysql.init_app(app) 
  mysql.app = app
  
  db.init_app(app)
  db.app = app

  socketio.init_app(app)

  
  migrate.init_app(app, db)
  migrate.app = app  
  
  from app_center.authentication.login import model, controller
  from app_center.backend.master import model_master
  from app_center.authentication.login import model
  from flask import jsonify
  from app_center.api import controller_api
  from app_center.cronjob import init_scheduler
    
  ''' INITIALIZE CRONJOB ''' 

  init_scheduler(app, DATABASE_FILE)
  
  login_manager = LoginManager()
  login_manager.init_app(app)  
  login_manager.login_view = 'login.login'
  
    
  @login_manager.user_loader
  def load_user(user_id):
    ''' since the user_id is just the primary key of our user table, use it in the query for the user '''
    user = model.User.query.get(int(user_id))
    if user == None:
      return user
    user.env = os.environ.get('FLASK_ENV')
    user.bearer_token = cmod.generateBearerToken(user.nik)
    therole = db.session.query(model_master.MasterRoles.role).filter_by(id=user.id_role).first()
    theakses = db.session.query(model.User).with_entities(model_master.MasterAksesManagement.id, model.User.nik, model_master.MasterAksesManagement.id_role, model_master.MasterRoles.role, 
                                                  model_master.MasterAksesManagement.id_page, model_master.MasterPages.page, model_master.MasterAksesManagement.akses, 
                                                  )\
                                                    .outerjoin(model_master.MasterAksesManagement, and_(model_master.MasterAksesManagement.nik==model.User.nik, model_master.MasterAksesManagement.id_role==model.User.id_role, model_master.MasterAksesManagement.status_aktif==1))\
                                                    .join(model_master.MasterRoles, and_(model_master.MasterRoles.id==model_master.MasterAksesManagement.id_role, model_master.MasterRoles.status_aktif==1))\
                                                    .join(model_master.MasterPages, and_(model_master.MasterPages.id==model_master.MasterAksesManagement.id_page, model_master.MasterPages.status_aktif==1))\
                                                    .filter(model.User.status_aktif==1,model.User.nik==user.nik).all()
    list_akses = []
    list_page = []
    if theakses:
      for ta in theakses:
        tdict = ta._asdict()
        if tdict['page'] not in list_page:
          list_page.append(tdict['page'])
        list_akses.append(f"{tdict['page']}-{tdict['akses']}")
    user.list_akses = list_akses
    user.list_page = list_page
    user.nama_roles = therole.role if therole else None    
    return user
  
  ''' REGISTER BLUEPRINTS OF APPLICATIONS '''
  app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
  ''' BLUEPRINT FRONTEND '''
  from app_center.route.frontend import register_frontend
  register_frontend(app)

  ''' BLUEPRINT BACKEND '''
  from app_center.route.backend import register_backend
  register_backend(app)
  
  ''' MODULES  '''
  app.add_url_rule('/get-progress', view_func=cmod.GetProgress.as_view("get_progress"), methods=['GET', 'POST'])
  app.add_url_rule('/flask-db-migrate', view_func=cmod.DBMigrate.as_view('db_migrate'), methods=['GET'])
  app.add_url_rule('/flask-db-upgrade', view_func=cmod.DBUpgrade.as_view('db_upgrade'), methods=['GET'])
  app.add_url_rule('/flask-db-reset', view_func=cmod.DBResetAlembic.as_view('db_reset'), methods=['GET'])
  app.add_url_rule('/git-pull', view_func=cmod.GitPull.as_view('git_pull'), methods=['GET'])
  app.add_url_rule('/systemctl-restart', view_func=cmod.SystemCTLRestart.as_view('systemctl_restart'), methods=['GET'])
  app.add_url_rule('/journalctl', view_func=cmod.JournalCTL.as_view('journalctl'), methods=['GET'])
  
  return app
