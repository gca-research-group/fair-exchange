import base64
import os
from uuid import uuid4

import requests
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from flask import Blueprint, Response, request

from project.repository import scoped_connection
from project.repository.models import Exchange

bp = Blueprint("exchange", __name__, url_prefix="/exchange")

# ========== private endpoints ==========


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


@bp.route("/<string:exchange_token>/send/", methods=["POST"])
def send(exchange_token: str):

    item = "Item da alice"

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

    signature = private_key.sign(
        encrypted_item,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    base_dir = f"attestable/{exchange_token}"

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

    with open(f"{base_dir}/encrypted.bin", "wb") as encrypted_file:
        encrypted_file.write(encrypted_item)

    with open(f"{base_dir}/signature", "wb") as encrypted_file:
        encrypted_file.write(signature)

    with open(f"{base_dir}/item", "w") as item_file:
        item_file.write(item)

    encrypted_b64 = base64.b64encode(encrypted_item).decode()
    signature_b64 = base64.b64encode(signature).decode()

    payload = {
        "encrypted_item": encrypted_b64,
        "signature": signature_b64,
        "public_key": public_pem.decode(),
    }

    response = requests.post(
        f"http://localhost:5001/api/exchange/{exchange_token}/item/", json=payload
    )

    if response.status_code != 200:
        return {"error": "Failed to send encrypted item to Bob"}, response.status_code

    return Response(status=200)


# ========== public endpoints ==========


@bp.route("/<string:exchange_token>/handshake/", methods=["POST"])
def handshake(exchange_token: str):

    with scoped_connection() as connection:

        user_token = uuid4()

        exchange = Exchange(token=exchange_token, user_token=user_token)

        connection.add(exchange)
        connection.commit()

    return Response(status=200)


@bp.route("/<string:exchange_token>/item/", methods=["POST"])
def item(exchange_token: str):
    data = request.get_json()

    encrypted_item = base64.b64decode(data["encrypted_item"])
    signature = base64.b64decode(data["signature"])
    public_key = serialization.load_pem_public_key(data["public_key"].encode())

    try:
        public_key.verify(
            signature,
            encrypted_item,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
    except InvalidSignature:
        return {
            "message": "Signature is invalid. Keys do not match or data was tampered."
        }, 400

    base_dir = f"attestable/{exchange_token}/bob"
    os.makedirs(base_dir, exist_ok=True)

    with open(os.path.join(base_dir, "encrypted.bin"), "wb") as file:
        file.write(encrypted_item)

    with open(os.path.join(base_dir, "public_key.pem"), "wb") as file:
        file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

    with open(os.path.join(base_dir, "signature"), "wb") as file:
        file.write(signature)

    return Response(status=200)
