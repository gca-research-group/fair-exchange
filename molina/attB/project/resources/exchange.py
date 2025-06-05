import os

from flask import Blueprint, Response, request

bp = Blueprint("exchange", __name__, url_prefix="/exchange")


@bp.route("/<string:exchange_token>/deposit", methods=["POST"])
def deposit(exchange_token: str):

    data = request.get_json()

    base_dir = f"data/{exchange_token}"

    os.makedirs(base_dir, exist_ok=True)

    with open(f"{base_dir}/encrypted_item", "w") as item_file:
        item_file.write(data.get("encrypted_item"))

    verify(data.get("values", {}))

    return Response(status=200)


@bp.route("/<string:exchange_token>/retrieve", methods=["GET"])
def retrieve(exchange_token: str):

    path = f"data/{exchange_token}/encrypted_item"

    if not os.path.exists(path):
        return Response("File not found", status=404)

    with open(path, "r") as item_file:
        content = item_file.read()

    return Response(content, status=200, mimetype="text/plain")


def verify(values):
    doc_value_types = {
        "value1": str,
        "value2": str,
        "value3": str,
    }

    value1 = values.get("value1", None)
    value2 = values.get("value2", None)
    value3 = values.get("value3", None)

    if not value1 or not isinstance(value1, doc_value_types["value1"]):
        raise ValueError("value1 is required and must be a string")

    if not value2 or not isinstance(value2, doc_value_types["value2"]):
        raise ValueError("value2 is required and must be a string")

    if not value3 or not isinstance(value3, doc_value_types["value3"]):
        raise ValueError("value3 is required and must be a string")

    if value1 != "value1":
        raise ValueError("value1 must be 'value1'")

    if value2 != "value2":
        raise ValueError("value2 must be 'value2'")

    if value3 != "value3":
        raise ValueError("value3 must be 'value3'")

    return True
