import uuid

from sqlalchemy import ForeignKey, String, Text, types, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


from enum import Enum as PyEnum

# Создаем Python Enum для типов счетов
class AccountType(str, PyEnum):
    DEBIT = "debit"
    SAVINGS = "savings"
    CREDIT = "credit"
    LOAN_OWED = "loan_owed"
    LOAN_LENT = "loan_lent"

class Account(Base):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4)
    currency: Mapped[str] = mapped_column(String(25), nullable=False)
    balance: Mapped[float] = mapped_column()
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    interest_rate: Mapped[float] = mapped_column()
    is_emergency_fund: Mapped[bool] = mapped_column(default=False)
    decimal_places: Mapped[int] = mapped_column(default=2)
    is_archived: Mapped[bool] = mapped_column(default=False)
    is_primary: Mapped[bool] = mapped_column(default=False)

    account_type: Mapped[AccountType] = mapped_column(Enum(AccountType), nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="accounts")
