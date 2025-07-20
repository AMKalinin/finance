from uuid import UUID

from pydantic import BaseModel

from app.models.account import AccountType
from app.schemas.transaction import transaction_in


class account_in(BaseModel):
    name: str
    currency: str
    balance: float = 0
    description: str | None = None
    interest_rate: int | None = None
    is_emergency_fund:bool = False
    decimal_places:int = 2
    is_archived: bool = False
    is_primary: bool = False
    account_type: AccountType
    transaction_info: transaction_in


class account_in_name(BaseModel):
    id: UUID
    name: str


class account_in_balance(BaseModel):
    id: UUID
    operation: str
    balance: float


class account_in_description(BaseModel):
    id: UUID
    description: str


class account_in_interest_rate(BaseModel):
    id: UUID
    interest_rate: int | None


class account_in_emergency_fund(BaseModel):
    id: UUID
    is_emergency_fund:bool 


class account_in_decimal_places(BaseModel):
    id: UUID
    decimal_places:int


class account_in_archived(BaseModel):
    id: UUID
    is_archived:bool


class account_in_primary(BaseModel):
    id: UUID
    is_primary:bool


class account_out(BaseModel):
    id: UUID
    currency: str
    name: str
    balance: float
    description: str
    interest_rate: int
    is_emergency_fund:bool
    decimal_places:int
    is_archived: bool
    is_primary: bool
    account_type: AccountType
