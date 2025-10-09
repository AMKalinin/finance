import datetime
import uuid

from sqlalchemy import ForeignKey, String, Text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Transaction_type(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)


class Split_type(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)


class Transaction_status(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)


class Transaction(Base):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4)
    FROM: Mapped[uuid.UUID] = mapped_column(ForeignKey("account.id"), nullable=True)
    TO: Mapped[uuid.UUID] = mapped_column(ForeignKey("account.id"), nullable=True)
    category: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True) 
    type: Mapped[str] = mapped_column(ForeignKey("transaction_type.name"), nullable=False)
    debit_size: Mapped[float] = mapped_column()
    credit_size: Mapped[float] = mapped_column()
    exchange_rate: Mapped[float] = mapped_column()
    date: Mapped[datetime.date] = mapped_column(default=datetime.date.today, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    split_type: Mapped[str] = mapped_column(ForeignKey("split_type.name"), nullable=True)
    status: Mapped[str] = mapped_column(ForeignKey("transaction_status.name"), nullable=True) 
    related_transactions: Mapped[uuid.UUID] = mapped_column(ForeignKey("transaction.id"), nullable=True)

    transaction_distribution_user = relationship("Transaction_distribution_user", back_populates="transactions")
    positions = relationship("Position", back_populates="transactions")
    # user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    # user = relationship("User", back_populates="transactions")
