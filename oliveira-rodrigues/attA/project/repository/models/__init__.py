from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    event,
)
from sqlalchemy.dialects.postgresql import UUID

from project.repository import db


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.now, nullable=False)


@event.listens_for(BaseModel, "before_insert", propagate=True)
def before_insert(_mapper, _connection, target: BaseModel):
    try:
        if target.created_at is None:
            target.created_at = datetime.now()
    except:
        pass
