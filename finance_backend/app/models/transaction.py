import datetime
import uuid

from sqlalchemy import ForeignKey, Text, types
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Transaction(Base):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4)
    FROM: Mapped[uuid.UUID] = mapped_column(ForeignKey("account.id"), nullable=True)
    TO: Mapped[uuid.UUID] = mapped_column(ForeignKey("account.id"), nullable=True)
    category: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)
    type_name: Mapped[str] = mapped_column(ForeignKey("type_transaction.name"), nullable=True)
    size: Mapped[float] = mapped_column()
    rate: Mapped[float] = mapped_column(nullable=True)
    date: Mapped[datetime.date] = mapped_column(default=datetime.date.today, nullable=False)
    description: Mapped[str] = mapped_column(Text)
