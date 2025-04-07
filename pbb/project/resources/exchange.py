from uuid import uuid4

from cryptography.hazmat.primitives import serialization
from flask import Blueprint, request
from werkzeug.exceptions import (
    BadRequest,
    Forbidden,
    NotFound,
)

from project.repository import scoped_connection
from project.repository.models import Exchange, ExchangeUser

bp = Blueprint("exchange", __name__, url_prefix="/exchange")


@bp.route("/", methods=["POST"])
def create():

    data = request.get_json()
    exchange_token = data.get("exchange_token")
    user_token = data.get("user_token")

    with scoped_connection() as connection:

        exchange_token = uuid4()
        user_token = uuid4()

        exchange = Exchange(token=exchange_token)

        connection.add(exchange)
        connection.flush()

        user = ExchangeUser(exchange_id=exchange.id, token=user_token)

        connection.add(user)

        connection.commit()

    return {}, 201


@bp.route("/<string:exchange_token>/user/<string:user_token>", methods=["POST"])
def add_user(exchange_token, user_token):
    with scoped_connection() as connection:
        exchange = connection.query(Exchange).filter_by(token=exchange_token).first()
        if not exchange:
            raise NotFound("Exchange not found")

        user = ExchangeUser(exchange_id=exchange.id, token=user_token)
        connection.add(user)
        connection.commit()

    return {}, 201


@bp.route("/<string:exchange_token>/<string:user_token>/accept", methods=["POST"])
def accept(exchange_token, user_token):
    with scoped_connection() as connection:
        user = connection.query(ExchangeUser).filter_by(token=user_token).first()
        verify_if_the_user_belongs_to_exchange(exchange_token, user_token)

        user.status = True
        connection.commit()
    return {}, 201


@bp.route("/<string:exchange_token>/<string:user_token>/reject", methods=["POST"])
def reject(exchange_token, user_token):
    with scoped_connection() as connection:
        user = connection.query(ExchangeUser).filter_by(token=user_token).first()
        verify_if_the_user_belongs_to_exchange(exchange_token, user_token)

        user.status = False
        connection.commit()
    return {}, 201


@bp.route("/<string:exchange_token>/<string:user_token>/private-key", methods=["POST"])
def add_private_key(exchange_token, user_token):
    data = request.get_json()
    private_key = data.get("private_key")
    if not private_key:
        raise BadRequest("Private key is required")
    with scoped_connection() as connection:
        user = connection.query(ExchangeUser).filter_by(token=user_token).first()
        verify_if_the_user_belongs_to_exchange(exchange_token, user_token)

        user.private_key = private_key
        connection.commit()


@bp.route("/<string:exchange_token>/<string:user_token>/private-key", methods=["POST"])
def verify_private_key(exchange_token, user_token):
    data = request.get_json()
    public_key = data.get("public_key")
    if not public_key:
        raise BadRequest("Public key is required")

    with scoped_connection() as connection:
        user = connection.query(ExchangeUser).filter_by(token=user_token).first()
        verify_if_the_user_belongs_to_exchange(exchange_token, user_token)

        try:
            private_key_obj = serialization.load_pem_private_key(
                user.private_key.encode(), password=None
            )

            derived_public_key = (
                private_key_obj.public_key()
                .public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
                .decode()
            )

            if user.public_key != derived_public_key:
                raise Forbidden("Public key does not match the private key")

        except Exception as e:
            raise BadRequest(f"Error verifying keys: {str(e)}")

    return {}, 200


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
