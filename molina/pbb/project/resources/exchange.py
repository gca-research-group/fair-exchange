from flask import Blueprint, Response, request
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

from project.repository import scoped_connection
from project.repository.models import (
    Exchange,
    ExchangeUser,
    ExchangeUserAcceptance,
)

bp = Blueprint("exchange", __name__, url_prefix="/exchange")


@bp.route("/<string:exchange_token>/acceptance", methods=["GET"])
def acceptance(exchange_token):
    with scoped_connection() as connection:
        exchange = connection.query(Exchange).filter_by(token=exchange_token).first()
        if not exchange:
            raise NotFound("Exchange not found")

        acceptances = (
            connection.query(ExchangeUserAcceptance)
            .filter_by(exchange_id=exchange.id)
            .all()
        )

        data = []

        for acceptance in acceptances:
            data.append(
                {
                    "user_name": acceptance.exchange_user.name,
                    "status": acceptance.status,
                }
            )

        return data, 200


@bp.route("/", methods=["POST"])
def create():

    data = request.get_json()
    exchange_token = data.get("exchange_token")
    user_token = data.get("user_token")
    user_name = data.get("user_name")

    if not exchange_token or not user_token or not user_name:
        raise BadRequest("exchange_token, user_token, and user_name are required")

    with scoped_connection() as connection:

        existing_exchange = (
            connection.query(Exchange).filter_by(token=exchange_token).first()
        )
        if existing_exchange:
            raise BadRequest("Exchange with this token already exists")

        exchange = Exchange(token=exchange_token)

        connection.add(exchange)
        connection.flush()

        user = ExchangeUser(exchange_id=exchange.id, token=user_token, name=user_name)

        connection.add(user)

        connection.commit()

    return Response(status=201)


@bp.route("/<string:exchange_token>/user/<string:user_token>", methods=["POST"])
def add_user(exchange_token, user_token):
    user_name = request.get_json().get("user_name")

    if not user_name:
        raise BadRequest("user_name is required")

    with scoped_connection() as connection:
        exchange = connection.query(Exchange).filter_by(token=exchange_token).first()
        if not exchange:
            raise NotFound("Exchange not found")

        user = ExchangeUser(exchange_id=exchange.id, token=user_token, name=user_name)
        connection.add(user)
        connection.commit()

    return Response(status=201)


@bp.route("/<string:exchange_token>/<string:user_token>/accept", methods=["PUT"])
def accept(exchange_token, user_token):
    with scoped_connection() as connection:
        user = connection.query(ExchangeUser).filter_by(token=user_token).first()
        verify_if_the_user_belongs_to_exchange(exchange_token, user_token)

        exchange_user_acceptance = ExchangeUserAcceptance(
            exchange_id=user.exchange_id, user_id=user.id, status=True
        )
        connection.add(exchange_user_acceptance)
        connection.commit()

    return Response(status=200)


@bp.route("/<string:exchange_token>/<string:user_token>/reject", methods=["PUT"])
def reject(exchange_token, user_token):
    with scoped_connection() as connection:
        user = connection.query(ExchangeUser).filter_by(token=user_token).first()
        verify_if_the_user_belongs_to_exchange(exchange_token, user_token)

        exchange_user_acceptance = ExchangeUserAcceptance(
            exchange_id=user.exchange_id, user_id=user.id, status=False
        )
        connection.add(exchange_user_acceptance)
        connection.commit()
    return Response(status=200)


def verify_if_the_user_belongs_to_exchange(exchange_token, user_token):
    with scoped_connection() as connection:
        exchange = connection.query(Exchange).filter_by(token=exchange_token).first()
        if not exchange:
            raise NotFound("Exchange not found")

        user = connection.query(ExchangeUser).filter_by(token=user_token).first()
        if not user:
            raise NotFound("User not found")

        if user.exchange_id != exchange.id:
            raise Forbidden("User does not belong to this exchange")

    return Response(status=200)
