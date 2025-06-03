from flask import Blueprint

from project.resources import exchange, healthcheck

bp = Blueprint("api", __name__, url_prefix="/api")

bp.register_blueprint(healthcheck.bp)
bp.register_blueprint(exchange.bp)
