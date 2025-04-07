import os
from uuid import uuid4

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from flask import Blueprint, request

from project.repository import scoped_connection
from project.repository.models import Exchange

bp = Blueprint("exchange", __name__, url_prefix="/exchange")


@bp.route("/", methods=["POST"])
def create():
    exchange_token = None
    try:
        data = request.json
        exchange_token = data.get("token", None)
    except:
        pass


    with scoped_connection() as connection:

        exchange_token = exchange_token if exchange_token is not None else uuid4()
        user_token = uuid4()

        exchange = Exchange(token=exchange_token, user_token=user_token)

        connection.add(exchange)
        connection.flush()

        connection.refresh(exchange)

    return {"exchange_token": exchange_token, "user_token": user_token}, 201


@bp.route("/<token>/handshake/", methods=["POST"])
def handshake(token: str):

    response = requests.post(
        f"http://localhost:5002/api/exchange/", json={"token": token}
    )

    if response.status_code != 201:
        return {"error": "Failed to perform handshake with Alice"}, response.status_code

    return {}, 200


@bp.route("/<token>/send/", methods=["POST"])
def send(token: str):

    item = "Item do bob"

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    public_key = private_key.public_key()

    encrypted_item = public_key.encrypt(
        item.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    base_dir = f"attestable/{token}"

    os.makedirs(base_dir, exist_ok=True)

    with open(f"{base_dir}/public_key.pem", "wb") as public_key_file:
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        public_key_file.write(public_pem)

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    with open(f"{base_dir}/private_key.pem", "wb") as private_key_file:
        private_key_file.write(private_pem)

    with open(f"{base_dir}/encrypted.bin", "wb") as encrypted_file:
        encrypted_file.write(encrypted_item)

    with open(f"{base_dir}/item", "w") as item_file:
        item_file.write(item)

    response = requests.post(
        f"http://localhost:5002/api/exchange/{token}/item/", data=encrypted_item
    )

    if response.status_code != 200:
        return {"error": "Failed to send encrypted item to Alice"}, response.status_code

    return {}, 200


@bp.route("/<token>/item/", methods=["POST"])
def item(token: str):
    base_dir = f"attestable/{token}/alice"
    os.makedirs(base_dir, exist_ok=True)

    with open(os.path.join(base_dir, "encrypted.bin"), "wb") as file:
        file.write(request.data)

    return {}, 200
