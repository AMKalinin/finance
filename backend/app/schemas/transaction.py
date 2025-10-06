import datetime
from uuid import UUID
from typing import Literal
from pydantic import BaseModel, Field


class Distribution(BaseModel):
    user_id: UUID
    role: Literal['owner', 'participant']
    size: float


class transaction_in(BaseModel):
    FROM: UUID | None
    TO: UUID | None
    category: UUID | None
    type: Literal['debit', 'adding', 'transfer'] | None = Field(alias="typeName")
    debit_size: float
    credit_size: float | None
    exchange_rate: float = Field(alias="exchangeRate")
    date: datetime.date
    description: str | None
    split_type: Literal['equal', 'percentage', 'amount', 'position']
    status: Literal['pending', 'partially_paid', 'settled']
    related_transactions: UUID | None
    distributions: list[Distribution]


class transaction_in_type(BaseModel):
    id: UUID
    FROM: UUID | None = None
    TO: UUID | None = None
    category: UUID | None = None
    type_name: str = Field(alias="typeName")


class transaction_in_size(BaseModel):
    id: UUID
    size: int


class transaction_in_date(BaseModel):
    id: UUID
    date: datetime.date


class transaction_in_category(BaseModel):
    id: UUID
    category: int


class transaction_in_description(BaseModel):
    id: UUID
    description: str


class transaction_in_delete(BaseModel):
    id: UUID


class transaction_out(BaseModel):
    id: UUID
    FROM: UUID | None
    TO: UUID | None
    size: float
    exchange_rate: float
    date: datetime.date
    category: UUID | None
    type_name: str = Field(serialization_alias="typeName")
    description: str
