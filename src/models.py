import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date

database_name = "capstone"
database_path = "postgres://{}:{}@{}/{}".format(
    'postgres', 'elang12', 'localhost:5432', database_name)

db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Actors

'''
class Actor(db.Model):
    __tablename__ = 'Actor'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80))
    role = Column(String(80))
    gender = Column(String(80))

    def insert(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'role': self.role
        }


class Movie(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80))
    year = Column(Integer)
    director = Column(String(80))
    genre = Column(String(180))

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'director': self.director,
            'genre': self.genre
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())