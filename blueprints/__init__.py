from flask import Flask, request
import json

##database import###
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_migrate import Manager

##JWT import
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta

#wrap
from functools import wraps

#Load ENV Python
import os
from dotenv import load_dotenv
load_dotenv()

# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only
from flask_cors import CORS

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


app = Flask(__name__)
app.config['APP_DEBUG'] = True
CORS(app)

#################
# JWT
###############

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=31)

jwt = JWTManager(app)
    
def intern_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] == "intern":
            return fn(*args, **kwargs)
        else:
            return {'status':'failed', 'message':'forbidden | internship Only'}, 403
    return wrapper


def company_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] == 'company':
            return fn(*args, **kwargs)
        else:
            return {'status':'failed', 'message':'forbidden | company only'}, 403

    return wrapper


####Database####


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:masukaja@0.0.0.0:3306/flaskstarter'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(os.getenv("DATABASE_USER"), os.getenv("DATABASE_PASSWORD"), os.getenv("DATABASE_HOST"), os.getenv("DATABASE_PORT"),  os.getenv("DATABASE_NAME"))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)  # command 'db' dapat menjalankan semua command MigrateCommand

###########Middleware#############
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    app.logger.warning("REQUEST_LOG\t%s", 
        json.dumps({
            'uri':request.full_path,
            'code':response.status,
            'method':request.method,
            'request':requestData,
            'response':json.loads(response.data.decode('utf-8'))}))

    return response


###############################
# Import blueprints
###############################

from blueprints.Auth import bp_auth
from blueprints.Intern.resources import bp_intern
from blueprints.Company.resources import bp_company
from blueprints.Position.resources import bp_position
from blueprints.Task.resources import bp_task
from blueprints.OngoingPosition.resources import bp_ongoing_position
from blueprints.ChoosePosition.resources import bp_choose_position
from blueprints.OngoingTask.resources import bp_ongoing_task
from blueprints.App.OnGoingPositionAndTask import bp_on_going_pos_task
from blueprints.App.ProcessDoneTask import bp_done_task
from blueprints.Certificate.resources import bp_certificate
from blueprints.App.CompanyAcceptance import bp_company_accept

app.register_blueprint(bp_auth, url_prefix='/login')
app.register_blueprint(bp_intern, url_prefix='/intern' )
app.register_blueprint(bp_company, url_prefix='/company' )
app.register_blueprint(bp_position, url_prefix='/position' )
app.register_blueprint(bp_task, url_prefix='/task' )
app.register_blueprint(bp_ongoing_position, url_prefix='/ongoingposition' )
app.register_blueprint(bp_choose_position, url_prefix='/chooseposition' )
app.register_blueprint(bp_ongoing_task, url_prefix='/ongoingtask' )
app.register_blueprint(bp_on_going_pos_task, url_prefix='/ongoingtaskposition' )
app.register_blueprint(bp_done_task, url_prefix='/donetask' )
app.register_blueprint(bp_certificate, url_prefix='/certificate' )
app.register_blueprint(bp_company_accept, url_prefix='/companyaccept' )


db.create_all()