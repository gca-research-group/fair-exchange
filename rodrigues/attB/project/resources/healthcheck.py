from flask import Blueprint

bp = Blueprint("healthcheck", __name__)


@bp.route("/healthcheck/", methods=["GET"])
def healthcheck():
    return {"message": "ok"}, 200
