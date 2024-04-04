from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Type(Base):
    # Пополнение\ списание \ перевод
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
