import uuid
from datetime import datetime

from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Exchange_rate(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid, primary_key=True, default=uuid.uuid4
    )
    from_currency_name: Mapped[str] = mapped_column(ForeignKey("currency.name"))
    to_currency_name: Mapped[str] = mapped_column(ForeignKey("currency.name"))
    rate: Mapped[float] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column()
