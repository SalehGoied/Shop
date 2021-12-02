from datetime import date, datetime, timedelta
from time import timezone
from sqlalchemy.sql import func

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date
import os
from sqlalchemy.sql.expression import false

#path of database

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
DB_USER = os.getenv('DB_USER', 'postgres')  
DB_PASSWORD = os.getenv('DB_PASSWORD', '01558125032saleh')  
DB_NAME = os.getenv('DB_NAME', 'shop')  
DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)


db = SQLAlchemy()

#setup database and config it

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


#drob and create all table

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

#create table

class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(10000), nullable=False)
    price = db.Column(db.Float(), nullable= False)
    quantity = db.Column(db.Integer(), nullable=False, default=0)
    order = db.relationship('Order', backref='product', lazy=True)
    
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Client(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(10000), nullable=False)
    phone = db.Column(db.String(50))
    address = db.Column(db.String(1000))
    amount = db.Column(db.Float(), nullable=False, default=0)
    history = db.relationship('History', backref='client', lazy=True)

    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class History(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), default=datetime.now())
    amount = db.Column(db.Float(), nullable=False, default=0)
    check_out = db.Column(db.Boolean(), default=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    order = db.relationship('Order', backref='history', lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer(), nullable=False, default=0)
    price = db.Column(db.Float(), nullable= False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

