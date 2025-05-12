import datetime
import uuid

from sqlalchemy import ForeignKey, String, Text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Transaction(Base):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4)
    FROM: Mapped[uuid.UUID] = mapped_column(ForeignKey("account.id"), nullable=True)
    TO: Mapped[uuid.UUID] = mapped_column(ForeignKey("account.id"), nullable=True)
    category: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)
    type_name: Mapped[str] = mapped_column(String(10), nullable=False)
    size: Mapped[float] = mapped_column()
    exchange_rate: Mapped[float] = mapped_column()
    date: Mapped[datetime.date] = mapped_column(default=datetime.date.today, nullable=False)
    description: Mapped[str] = mapped_column(Text)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="transactions")
