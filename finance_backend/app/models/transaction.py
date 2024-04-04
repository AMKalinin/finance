import datetime
import uuid

from sqlalchemy import ForeignKey, Text, types
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Transaction(Base):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4())
    FROM: Mapped[uuid.UUID] = mapped_column(ForeignKey("accaunt.id"), nullable=True)
    TO: Mapped[uuid.UUID] = mapped_column(ForeignKey("accaunt.id"), nullable=True)
    size: Mapped[float] = mapped_column()
    data: Mapped[datetime.date] = mapped_column(nullable=False)
    category: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)
    type: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)
    description: Mapped[str] = mapped_column(Text)
