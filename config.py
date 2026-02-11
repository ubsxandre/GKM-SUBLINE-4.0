import os, pymysql
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists,create_database
# linux to windows

string_json_schwarzenegger = """{
  "swagger": "2.0",
  "info": {
    "title": "Access API",
    "version": "1.0.0"
  },
  "paths": {
    "/api/login": {
     "$ref":"./login.json"
    }
  }
}
"""

string_json_login = """{
  "post": {
    "description": "Login User using SSO account",
    "consumes": [
      "application/json"
    ],
    "produces": [
      "application/json"
    ],
    "parameters": [
      {
        "name": "JSON nik-pass",
        "in": "body",
        "description": "JSON data for login",
        "required": true,
        "schema": {
                    "type": "object",
                    "properties": {
                      "nik": {
                        "type": "string"
                      },
                      "password": {
                        "type": "string"
                      }
                    }
                  }
      }
    ],
    "responses": {
      "200": {
        "description": "User granted access"
      },
      "400": {
        "description": "Invalid request data"
      }
    }
  }
}"""

''' SET THE BASE DIRECTORY '''
BASEDIR = os.path.abspath(os.path.dirname(__file__))

''' SET CREATE FOLDER '''
def createFolder(PATH):
  folderPath = os.path.join(BASEDIR, PATH)
  os.makedirs(folderPath)

''' AUTO CREATE NAME DB '''
def validateDatabase(DATABASE_FILE, DB_NAME):
  engine = create_engine(DATABASE_FILE)
  if not database_exists(engine.url): # Checks for the first time  
    create_database(engine.url)     # Create new DB    
    print(f"{DB_NAME} Database Created") # Verifies if database is there or not.
  else:
    print(f"Database {DB_NAME} Running")

# Create the super class
class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY')
  # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
  # SQLALCHEMY_TRACK_MODIFICATIONS = False
  
  
''' DEVELOPMENT CONFIG '''
class DevelopmentConfig(Config):
  DEBUG = True
  SECRET_KEY = os.environ.get('SECRET_KEY')

  LOGS_FOLDER = "./app_center/static/logs/"
  CEK_LOGS_FOLDER = os.path.exists(LOGS_FOLDER)
  GITIGNORE_PATH = os.path.join(LOGS_FOLDER, '.gitignore')
  CEK_GITIGNORE = os.path.exists(GITIGNORE_PATH)

  if not CEK_LOGS_FOLDER:
    createFolder(LOGS_FOLDER)
    print(f"Folder Logs Telah Dibuat")
  
  if not CEK_GITIGNORE and CEK_LOGS_FOLDER == True:
    with open(GITIGNORE_PATH, 'w+') as f:
      f.write("*\n*/\n!.gitignore")
    print("File Gitignore untuk logs telah dibuat")
  
  
  SWAGGER_FOLDER = "./app_center/static/swagger"  
  SWAGGER_JSON = "./app_center/static/swagger/!swagger-main.json"
  SWAGGER_LOGIN_JSON = "./app_center/static/swagger/login.json"
  CEK_FOLD_SWAG = os.path.exists(SWAGGER_FOLDER)
  if not CEK_FOLD_SWAG:
    createFolder(SWAGGER_FOLDER)
    print(f"Folder swagger Telah Dibuat")
    
  
  CEK_SWAG = os.path.exists(SWAGGER_JSON)
  if not CEK_SWAG:
    with open(SWAGGER_JSON, 'w+') as f:
      f.write(string_json_schwarzenegger)  
    print("File json untuk swagger telah dibuat")
  
  CEK_SWAG_LOGIN = os.path.exists(SWAGGER_LOGIN_JSON)
  if not CEK_SWAG:
    with open(SWAGGER_LOGIN_JSON, 'w+') as f:
      f.write(string_json_login)  
    print("File json untuk swagger login telah dibuat")
  
  FOLDER_FILES_FOLDER = []
  FOLDER_FILES = "./app_center/static/files"
  if not os.path.exists(FOLDER_FILES):
    createFolder(FOLDER_FILES)
    print("Folder files telah dibuat")
    if not os.path.exists(os.path.join(FOLDER_FILES, ".gitignore")):
      with open(os.path.join(FOLDER_FILES, ".gitignore"), 'w+') as f:
        f.write("*\n*/\n!.gitignore")
      print("File Gitignore untuk files telah dibuat")
  
  for fnaf in FOLDER_FILES_FOLDER:
    if not os.path.exists(os.path.join(FOLDER_FILES, fnaf)):
      createFolder(os.path.join(FOLDER_FILES, fnaf))
      print(f"Folder Files {fnaf} telah dibuat")


  HOST = str(os.environ.get("DB_HOST"))
  DATABASE = str(os.environ.get("DB_DATABASE"))
  DATABASE_HISTORY = str(os.environ.get("DB_DATABASE_HISTORY"))
  USERNAME = str(os.environ.get("DB_USERNAME"))
  PASSWORD = str(os.environ.get("DB_PASSWORD"))
  
  DATABASE_FILE = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}'
  DATABASE_FILE_HISTORY = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE_HISTORY}'
  validateDatabase(DATABASE_FILE, DATABASE)
  validateDatabase(DATABASE_FILE_HISTORY, DATABASE_HISTORY)
  SQLALCHEMY_DATABASE_URI = DATABASE_FILE
  SQLALCHEMY_BINDS = {
    "history": DATABASE_FILE_HISTORY
  }
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_RECORD_QUERIES = True 
  