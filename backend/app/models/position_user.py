import uuid

from sqlalchemy import ForeignKey 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Position_user(Base):
    position_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('position.id'), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'), primary_key=True)
    quantity: Mapped[int] = mapped_column()

    positions = relationship('Position', back_populates='position_shares')
    user = relationship('User', back_populates='position_shares')
