import bcrypt


def hash(token: str):
    salt = bcrypt.gensalt()
    return str(bcrypt.hashpw(str(token).encode("utf-8"), salt), "utf-8")


def verify_hash(hash: bytes, token: bytes) -> bool:
    return bcrypt.checkpw(token, bytes(hash, "utf-8"))
