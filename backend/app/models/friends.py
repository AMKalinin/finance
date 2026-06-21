import uuid
from datetime import datetime

from sqlalchemy import Index, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Friends_status(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)


class Friends(Base):
    user1_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'), primary_key=True, index=True)
    user2_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'), primary_key=True, index=True)
    status: Mapped[str] = mapped_column(ForeignKey('friends_status.name'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)

    user1 = relationship('User', foreign_keys=[user1_id], backref='friends_sent')
    user2 = relationship('User', foreign_keys=[user2_id], back_populates='friends')

    __table_args__ = (
        Index('ix_friends_user1_status', 'user1_id', 'status'),
        Index('ix_friends_user2_status', 'user2_id', 'status'),
    )
