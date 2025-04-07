import logging

from flask import Flask
from flask_migrate import Migrate
from werkzeug.exceptions import (
    BadRequest,
    HTTPException,
    Unauthorized,
    UnprocessableEntity,
)

from project import resources
from project.config import Config, file_handler
from project.handlers.exception import handle_exception, handle_http_exception
from project.repository import db

migrate = Migrate()


def create_app(config=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)


    app.register_blueprint(resources.bp)

    app.logger.addHandler(file_handler)
    logging.getLogger("sqlalchemy").addHandler(file_handler)

    @app.template_filter()
    def format_datetime(value, format_="%d/%m/%Y %H:%M"):
        return value.strftime(format_)

    app.register_error_handler(Unauthorized, handle_exception)
    app.register_error_handler(UnprocessableEntity, handle_exception)
    app.register_error_handler(BadRequest, handle_exception)
    app.register_error_handler(HTTPException, handle_http_exception)

    return app
