import uuid

from sqlalchemy import Text, types
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Accaunt(Base):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4())
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
