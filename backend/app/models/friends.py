import uuid

from sqlalchemy import Text, ForeignKey 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Friends_status(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)


class Friends(Base):
    user1_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'), primary_key=True)
    user2_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'), primary_key=True)
    status: Mapped[str] = mapped_column(ForeignKey('friends_status.name'))
    
    user2 = relationship('User', foreign_keys=[user2_id], back_populates='friends')
