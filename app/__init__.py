import os
from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lab5:pa$sword@localhost/lab5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views