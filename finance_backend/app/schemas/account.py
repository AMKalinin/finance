from uuid import UUID

from pydantic import BaseModel


class account_in(BaseModel):
    name: str
    balance: float = 0
    description: str | None


class account_in_name(BaseModel):
    id: UUID
    name: str


class account_in_balance(BaseModel):
    id: UUID | None
    operation: str
    balance: float = 0


class account_in_description(BaseModel):
    id: UUID
    description: str | None


class account_out(BaseModel):
    id: UUID
    name: str
    balance: float
    description: str
