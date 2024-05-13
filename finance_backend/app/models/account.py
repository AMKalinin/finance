import uuid

from sqlalchemy import ForeignKey, Text, types
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Account(Base):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4)
    balance: Mapped[float] = mapped_column()
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.name"), nullable=False)
