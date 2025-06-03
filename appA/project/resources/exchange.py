import base64
import os
from uuid import uuid4

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from flask import Blueprint, Response, request

from project.repository import scoped_connection
from project.repository.models import Exchange

bp = Blueprint("exchange", __name__, url_prefix="/exchange")


ATTESTABLE_URL = "http://localhost:6001/api/exchange"
APP_B_URL = "http://localhost:7000/api/exchange"

@bp.route("/", methods=["POST"])
def create():
    with scoped_connection() as connection:

        exchange_token = uuid4()
        user_token = uuid4()

        exchange = Exchange(token=exchange_token, user_token=user_token)

        connection.add(exchange)
        connection.commit()

    return {"exchange_token": exchange_token, "user_token": user_token}, 201


@bp.route("/<string:exchange_token>", methods=["GET"])
def show(exchange_token: str):
    with scoped_connection() as connection:
        exchange = connection.query(Exchange).filter_by(token=exchange_token).first()

        if not exchange:
            return {"error": "Exchange not found"}, 404

        return {
            "exchange_token": exchange.token,
            "user_token": exchange.user_token,
        }, 200


@bp.route("/<string:exchange_token>/public-key", methods=["PATCH"])
def set_public_key(exchange_token: str):
    data = request.get_json()

    if not data or "public_key" not in data:
        return {"error": "Public key is required"}, 400

    public_key = data.get("public_key")

    with scoped_connection() as connection:
        exchange = connection.query(Exchange).filter_by(token=exchange_token).first()

        if not exchange:
            return {"error": "Exchange not found"}, 404

        exchange.public_key = public_key

        connection.add(exchange)
        connection.commit()

        return {"message": "Public key set successfully"}, 200


@bp.route("/<string:exchange_token>/public-key", methods=["POST"])
def send_public_key(exchange_token: str):
    with scoped_connection() as connection:
        exchange = connection.query(Exchange).filter_by(token=exchange_token).first()

        if not exchange:
            return {"error": "Exchange not found"}, 404

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        public_key = private_key.public_key()

        base_dir = f"keys/{exchange_token}"

        os.makedirs(base_dir, exist_ok=True)

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        with open(f"{base_dir}/public_key.pem", "wb") as public_key_file:
            public_key_file.write(public_pem)

        with open(f"{base_dir}/private_key.pem", "wb") as private_key_file:
            private_key_file.write(private_pem)

        payload = {
            "public_key": public_pem.decode(),
        }

        response = requests.patch(
            f"{APP_B_URL}/{exchange_token}/public-key",
            json=payload,
        )

        if response.status_code != 200:
            return {
                "error": "Failed to send encrypted item to the attestable"
            }, response.status_code

        return {"message": "Public key set successfully"}, 200


@bp.route("/<string:exchange_token>/send-item", methods=["POST"])
def send_item(exchange_token: str):

    with scoped_connection() as connection:
        exchange = connection.query(Exchange).filter_by(token=exchange_token).first()

        if not exchange:
            return {"error": "Exchange not found"}, 404

        if not exchange.public_key:
            return {"error": "Public key not set for the exchange"}, 400

        public_key = serialization.load_pem_public_key(exchange.public_key.encode())

        item = "Item App A"

        encrypted_item = public_key.encrypt(
            item.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        encrypted_b64 = base64.b64encode(encrypted_item).decode()

        payload = {
            "encrypted_item": encrypted_b64,
            "doc_value": {
                "value1": "value1",
                "value2": "value2",
                "value3": "value3",
            }
        }

        response = requests.post(
            f"{APP_B_URL}/{exchange_token}/send-attestable",
            json=payload,
        )

        if response.status_code != 200:
            return {
                "error": "Failed to send encrypted item to the attestable 1"
            }, response.status_code

        return Response(status=200)


@bp.route("/<string:exchange_token>/send-attestable", methods=["POST"])
def send_to_attestable(exchange_token: str):

    payload = request.get_json()

    with scoped_connection() as connection:
        exchange = connection.query(Exchange).filter_by(token=exchange_token).first()

        if not exchange:
            return {"error": "Exchange not found"}, 404

        if not exchange.public_key:
            return {"error": "Public key not set for the exchange"}, 400

        response = requests.post(
            f"{ATTESTABLE_URL}/{exchange_token}/deposit", json=payload
        )

        if response.status_code != 200:
            return {
                "error": "Failed to send encrypted item to the attestable 2"
            }, response.status_code

        return Response(status=200)


@bp.route("/<string:exchange_token>/handshake", methods=["POST"])
def handshake(exchange_token: str):

    with scoped_connection() as connection:

        user_token = uuid4()

        exchange = Exchange(token=exchange_token, user_token=user_token)

        connection.add(exchange)
        connection.commit()

    return Response(status=200)
