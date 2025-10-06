import uuid

from sqlalchemy import ForeignKey, String, Text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Distribution_status(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)

class Distribution_user_role(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)


class Transaction_distribution_user(Base):
    transaction_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('transaction.id'), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'), primary_key=True)
    distribution_user_role: Mapped[str] = mapped_column(ForeignKey('distribution_user_role.name'))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    size: Mapped[float] = mapped_column()
    #fraction: Mapped[bool] = mapped_column(default=False)

    transactions = relationship("Transaction", back_populates="transaction_distribution_user")
    user = relationship("User", back_populates="transaction_distribution_user")
