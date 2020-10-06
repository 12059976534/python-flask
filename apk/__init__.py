from flask import Flask,render_template,redirect,request,session,url_for,redirect
from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
import secrets
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
ckeditor = CKEditor(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:wahyu355@localhost/future'
app.secret_key=os.urandom(25)
db=SQLAlchemy(app)
migrate=Migrate(app,db)


from apk.model.db import Conten,User
from apk.controler.route import *