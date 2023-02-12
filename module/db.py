from module.app import app
from flask_sqlalchemy import SQLAlchemy

# import os
# from dotenv import load_dotenv
# load_dotenv()

db = SQLAlchemy()

user = 'developer'
password = 'c5nYkAWbgZmrBEXkk8EJe5nRiapVBV9d'
host = 'dpg-cfkahpda49903fn1jl5g-a.ohio-postgres.render.com'
port = '5432'
database = 'maindb_t4vn'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{database}'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
app.config['SECRET_KEY']= 'mySecretKey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db.init_app(app)


class User(db.Model):
    __tablename__ = "users" # table name in the database
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(150), nullable=False)

class Video(db.Model):
    __tablename__ = "videos" # table name in the database
    video_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_name  = db.Column(db.String(100), unique=True, nullable=False)
    video_url   = db.Column(db.String(150), unique=True, nullable=False)
    video_owner = db.Column(db.Integer, nullable=False)
    srt_url     = db.Column(db.String(150), unique=True, nullable=True)
    is_converted    = db.Column(db.Boolean, default=False)

# with app.app_context():
    #     db.create_all()

def addUser(user):
    db.session.add(user)
    db.session.commit()

def addVideo(video):
    db.session.add(video)
    db.session.commit()

def updateVideo():
    db.session.commit()
