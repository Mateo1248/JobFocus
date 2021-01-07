from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db(app):
    db.init_app(app)


def db_add(data):
    db.session.add(data)
    db.session.commit()


def db_delete(data):
    db.session.delete(data)
    db.session.commit()