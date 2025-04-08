import enum
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    event,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from project.repository import db


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.now, nullable=False)


class ExchangeStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"
    FAILED = "FAILED"
    FINISHED = "FINISHED"


@dataclass
class Exchange(BaseModel):
    __tablename__ = "exchange"

    token = Column(String, nullable=False, unique=True)
    status = Column(Enum(ExchangeStatus), nullable=False, default=ExchangeStatus.ACTIVE)


@dataclass
class ExchangeUser(BaseModel):
    __tablename__ = "exchange_user"

    token = Column(String, nullable=False)
    exchange_id = Column(UUID(as_uuid=True), ForeignKey("exchange.id"), nullable=False)
    private_key = Column(String, nullable=True)
    status = Column(Boolean, nullable=False, default=False)

    exchange = relationship(
        "Exchange",
        backref="exchange_user__exchange",
        foreign_keys=[exchange_id],
    )

    __table_args__ = (
        db.UniqueConstraint("token", "exchange_id", name="uq_exchange_user_token_exchange_id"),
    )


@event.listens_for(BaseModel, "before_insert", propagate=True)
def before_insert(_mapper, _connection, target: BaseModel):
    try:
        if target.created_at is None:
            target.created_at = datetime.now()
    except:
        pass
