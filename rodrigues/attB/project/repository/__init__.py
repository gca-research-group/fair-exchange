from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

db = SQLAlchemy(engine_options={"echo": True})


def get_engine(url: str = None, echo=True):
    if not url:
        url = current_app.config["SQLALCHEMY_DATABASE_URI"]
    return create_engine(url, echo=echo)


def scoped_connection():
    session = scoped_session(sessionmaker(bind=get_engine()))
    return session()
