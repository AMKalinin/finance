import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Category(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    type_category: Mapped[str] = mapped_column(String(10), nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="categories")
