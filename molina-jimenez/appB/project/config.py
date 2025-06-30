import logging
import os
from datetime import timedelta
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv

MAX_PAGES = 5
PAGE_SIZE = 100

load_dotenv()

DATABASE_HOST = os.environ.get("POSTGRES_HOST")
DATABASE_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DATABASE_NAME = os.environ.get("POSTGRES_DB")
DATABASE_USER = os.environ.get("POSTGRES_USER")
DATABASE_PORT = os.environ.get("POSTGRES_PORT")

if not os.path.exists("logs"):
    os.mkdir("logs")

formatter = logging.Formatter(
    "%(name)s | [%(asctime)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler = TimedRotatingFileHandler(
    os.path.join(os.getcwd(), "logs", "app.log"),
    when="midnight",
    interval=1,
    backupCount=7,
)

file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)


class Config:
    SESSION_TYPE = "filesystem"

    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get("SECRET_KEY")

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
