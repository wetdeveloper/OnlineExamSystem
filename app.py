import datetime
import uuid
from flask import Flask,render_template,url_for,request,redirect,jsonify,session
from flask_login import login_user,LoginManager,current_user,logout_user
from flask_sessionstore import Session
from flask_wtf import FlaskForm ,CSRFProtect,RecaptchaField
from wtforms import PasswordField,StringField, validators,SubmitField
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlalchemy.engine import Engine
from sqlalchemy import event,create_engine,or_,desc
from flask_bootstrap import Bootstrap  
from flask_login import UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_moment import Moment 


app=Flask(__name__, template_folder='static')
app.config['service_email_address']="your email address goes here"
app.config['service_email_appPassword']='your email app password goes here' #Like gmail app password

app.config['SECRET_KEY']='thisisehsanghgfhfdgd'
app.config['WTF_CSRF_SECRET_KEY']='wtffdjfksdjfksjg;jgkdlsgh'

login_manager=LoginManager()
login_manager.init_app(app)


app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']= '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
app.config['RECAPTCHA_PRIVATE_KEY']='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}

Bootstrap(app)
db = SQLAlchemy(app)
csrf=CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
app.config['SESSION_SQLALCHEMY'] = db
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection: 
       cursor = dbapi_connection.cursor()
       cursor.execute("PRAGMA foreign_keys=ON")
       cursor.close()

admin=Admin(app,name='My App',template_mode='bootstrap3')
engine=create_engine('sqlite:///DB.db')
Session(app)
moment=Moment(app)





if __name__=='__main__':
    app.run(debug='True')

