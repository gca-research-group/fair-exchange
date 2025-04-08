from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from flask import Blueprint, Response, request
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

from project.repository import scoped_connection
from project.repository.models import Exchange, ExchangeUser

bp = Blueprint("exchange", __name__, url_prefix="/exchange")


@bp.route("/", methods=["POST"])
def create():

    data = request.get_json()
    exchange_token = data.get("exchange_token")
    user_token = data.get("user_token")

    with scoped_connection() as connection:

        existing_exchange = (
            connection.query(Exchange).filter_by(token=exchange_token).first()
        )
        if existing_exchange:
            raise BadRequest("Exchange with this token already exists")

        exchange = Exchange(token=exchange_token)

        connection.add(exchange)
        connection.flush()

        user = ExchangeUser(exchange_id=exchange.id, token=user_token)

        connection.add(user)

        connection.commit()

    return Response(status=201)


@bp.route("/<string:exchange_token>/user/<string:user_token>", methods=["POST"])
def add_user(exchange_token, user_token):
    with scoped_connection() as connection:
        exchange = connection.query(Exchange).filter_by(token=exchange_token).first()
        if not exchange:
            raise NotFound("Exchange not found")

        user = ExchangeUser(exchange_id=exchange.id, token=user_token)
        connection.add(user)
        connection.commit()

    return Response(status=201)


@bp.route("/<string:exchange_token>/<string:user_token>/private-key", methods=["POST"])
def add_private_key(exchange_token, user_token):
    private_key = request.data.decode()

    if not private_key:
        raise BadRequest("Private key is required")

    with scoped_connection() as connection:
        user = connection.query(ExchangeUser).filter_by(token=user_token).first()
        verify_if_the_user_belongs_to_exchange(exchange_token, user_token)

        user.private_key = private_key
        connection.commit()

    return Response(status=201)


@bp.route("/<string:exchange_token>/verify-private-key", methods=["POST"])
def verify_private_key(exchange_token):
    public_key = request.data.decode()

    with scoped_connection() as connection:
        exchange = connection.query(Exchange).filter_by(token=exchange_token).first()
        if not exchange:
            raise NotFound("Exchange not found")

        users = connection.query(ExchangeUser).filter_by(exchange_id=exchange.id).all()

        if not users:
            raise NotFound("No users found for this exchange")

        is_valid = False

        for user in users:
            if is_valid:
                break

            try:
                loaded_public_key = serialization.load_pem_public_key(
                    public_key.encode()
                )

                loaded_private_key = serialization.load_pem_private_key(
                    user.private_key.encode(), password=None
                )

                ciphertext = loaded_public_key.encrypt(
                    "test".encode(),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None,
                    ),
                )

                loaded_private_key.decrypt(
                    ciphertext,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None,
                    ),
                )

                is_valid = True
            except:
                pass

    return Response(status=200 if is_valid else 403)


@bp.route("/<string:exchange_token>/<string:user_token>/accept", methods=["PUT"])
def accept(exchange_token, user_token):
    with scoped_connection() as connection:
        user = connection.query(ExchangeUser).filter_by(token=user_token).first()
        verify_if_the_user_belongs_to_exchange(exchange_token, user_token)

        user.status = True
        connection.commit()
    return Response(status=200)


@bp.route("/<string:exchange_token>/<string:user_token>/reject", methods=["PUT"])
def reject(exchange_token, user_token):
    with scoped_connection() as connection:
        user = connection.query(ExchangeUser).filter_by(token=user_token).first()
        verify_if_the_user_belongs_to_exchange(exchange_token, user_token)

        user.status = False
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


@bp.route("/<string:exchange_token>/private-keys", methods=["GET"])
def get_private_keys(exchange_token):
    with scoped_connection() as connection:
        exchange = connection.query(Exchange).filter_by(token=exchange_token).first()
        if not exchange:
            raise NotFound("Exchange not found")

        users = connection.query(ExchangeUser).filter_by(exchange_id=exchange.id).all()
        if not users:
            raise NotFound("No users found for this exchange")

        if not all(user.status for user in users):
            raise Forbidden("Not all users have accepted the exchange")

        private_keys = [user.private_key for user in users if user.private_key]

    return {"private_keys": private_keys}, 200