from uuid import uuid4

from flask import Blueprint

from project.repository import scoped_connection
from project.repository.exchange import find_by_token
from project.repository.models import Exchange, ExchangeUser
from project.utils.authentication import hash

bp = Blueprint("exchange", __name__, url_prefix="/exchange")


@bp.route("/", methods=["POST"])
def create():

    with scoped_connection() as connection:

        exchange_token = uuid4()
        user_token = uuid4()

        exchange = Exchange(token=hash(exchange_token))

        connection.add(exchange)
        connection.flush()

        user = ExchangeUser(exchange_id=exchange.id, token=hash(user_token))

        connection.add(user)

        connection.commit()

        connection.refresh(exchange)
        connection.refresh(user)

    return {"exchange_token": exchange_token, "user_token": user_token}, 201


@bp.route("/<token>/user/", methods=["POST"])
def add_user(token: str):

    with scoped_connection() as connection:

        exchange = find_by_token(connection, token)

        user_token = uuid4()

        user = ExchangeUser(exchange_id=exchange.id, token=hash(user_token))

        connection.add(user)

        connection.commit()

        connection.refresh(user)

    return {"exchange_token": exchange.token, "user_token": user.token}, 201
