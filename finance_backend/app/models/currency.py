from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Currency(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
