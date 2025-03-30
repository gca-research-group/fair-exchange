from sqlalchemy.orm import Session

from project.repository.models import Exchange


def find_by_token(connection: Session, token: str):
    return Exchange.query.filter(Exchange.token == token).scalar()
