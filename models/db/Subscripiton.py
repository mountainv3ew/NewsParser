from uuid import uuid4
from sqlalchemy import BigInteger, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from models.db.Base import Base


class ChannelSubscription(Base):
    __tablename__ = 'channels_subscriptions'

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(BigInteger)
    channel = mapped_column(String(length=40))
