import uuid

from sqlalchemy import ForeignKey, String, Text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Account(Base):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4)
    currency: Mapped[str] = mapped_column(String(25), nullable=False)
    balance: Mapped[float] = mapped_column()
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="accounts")
