from logging import error
from math import e
from os import name
from flask import Flask, render_template, redirect, request
from flask.helpers import flash
from .models import setup_db, db_drop_and_create_all
from flask_cors import CORS
from .views import views

app = Flask(__name__)
setup_db(app)
CORS(app)
app.config['SECRET_KEY'] = '**********'

# db_drop_and_create_all()



app.register_blueprint(views, url_prefix=('/'))

    