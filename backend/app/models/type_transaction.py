from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Type_transaction(Base):
    # Пополнение\ списание \ перевод
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)
