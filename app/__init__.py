from flask import Flask, render_template, request
from copy import deepcopy
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

db.init_app(app)

from app import models
from app.models import User, Film

