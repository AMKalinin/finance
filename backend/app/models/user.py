import uuid

from sqlalchemy import Text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4)
    description: Mapped[str] = mapped_column(Text)

    accounts = relationship("Account", back_populates="user", lazy="dynamic")
    categories = relationship("Category", back_populates="user", lazy="dynamic")
    transactions = relationship("Transaction", back_populates="user", lazy="dynamic")
