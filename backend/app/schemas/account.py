from uuid import UUID

from pydantic import BaseModel

from app.models.account import AccountType
from app.schemas.transaction import transaction_in


class BaseAccountModel(BaseModel):
    id: UUID


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
#    transaction_info: transaction_in


class account_in_name(BaseAccountModel):
    name: str


class account_in_balance(BaseAccountModel):
    operation: str
    balance: float


class account_in_description(BaseAccountModel):
    description: str


class account_in_interest_rate(BaseAccountModel):
    interest_rate: int | None


class account_in_emergency_fund(BaseAccountModel):
    is_emergency_fund:bool 


class account_in_decimal_places(BaseAccountModel):
    decimal_places:int


class account_in_archived(BaseAccountModel):
    is_archived:bool


class account_in_primary(BaseAccountModel):
    is_primary:bool


class account_out(BaseAccountModel):
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
