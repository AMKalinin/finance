import uuid
import json 
from datetime import date

from sqlalchemy import ForeignKey, Text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Subscription_type(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)


class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4)
    description: Mapped[str] = mapped_column(Text)
    subscription_type: Mapped[str] = mapped_column(ForeignKey('subscription_type.name'), default='free')
    subscription_expiry: Mapped[date] = mapped_column(nullable=True)
    accounts = relationship("Account", back_populates="user", lazy="dynamic")
    categories = relationship("Category", back_populates="user", lazy="dynamic")
    position_shares = relationship("Position_user", back_populates="user", lazy="dynamic")
    transaction_distribution_user = relationship(
        "Transaction_distribution_user",
        back_populates="user",
        lazy="dynamic"
    )

    #transactions = relationship("Transaction", back_populates="user", lazy="dynamic")
    friends = relationship("Friends",foreign_keys='Friends.user2_id', back_populates="user2")
