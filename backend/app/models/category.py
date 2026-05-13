import uuid

from sqlalchemy import ForeignKey, Index, String, Text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Category_type(Base):
    # Пополнение\ списание \ перевод
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)


class Category(Base):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(ForeignKey('category_type.name'), nullable=False, index=True)
    parent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("category.id"), nullable=True, index=True)
    #old_parent_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, nullable=True)
    level: Mapped[int] = mapped_column()
    is_deleted: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False, index=True)
    user = relationship("User", back_populates="categories")
    parent = relationship("Category", remote_side=[id], backref="children")

    __table_args__ = (
        Index('ix_category_user_type', 'user_id', 'type'),
        Index('ix_category_parent_level', 'parent_id', 'level'),
        Index('ix_category_user_is_deleted', 'user_id', 'is_deleted'),
    )
