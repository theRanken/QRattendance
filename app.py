import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from database import  db
from models import *
import logging
import datetime

BASE = os.path.dirname(__file__)
app = Flask(__name__, template_folder='./templates')
CSRFProtect(app)
app.secret_key = "j%a1w%keu83z__u+i$_w9^55ai-_vzx-dwr+z9*5=5j5a&c6ze"
app.config ['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE, 'app.db')}"
app.config['PERMANENT_SESSION_LIFETIME'] =datetime.timedelta(minutes=1440)
logging.basicConfig(level=logging.DEBUG)
app.app_context().push()
db.init_app(app)



