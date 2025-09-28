import datetime
import uuid

from sqlalchemy import ForeignKey, String, Text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Position(Base):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text)
    transaction_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("transaction.id"), nullable=False)
    price: Mapped[float] = mapped_column()
    quantity: Mapped[int] = mapped_column()

    transactions = relationship('Transaction', back_populates='positions')
    position_shares = relationship('Position_user', back_populates='positions')
