import datetime
from uuid import UUID
from typing import Literal
from pydantic import BaseModel, Field


class distribution_in(BaseModel):
    user_id: UUID = Field(alias='userId')
    transaction_id: UUID | None = Field(default=None, alias='transactionId')
    role: Literal['owner', 'participant'] = Field(default='participant')
    size: float | None = Field(default=None)


class distribution_out(BaseModel):
    user_id: UUID = Field(serialization_alias='userId')
    transaction_id: UUID = Field(serialization_alias='transactionId')
    distribution_user_role: Literal['owner', 'participant'] = Field(serialization_alias='role')
    size: float



class transaction_in(BaseModel):
    FROM: UUID | None = Field(default=None)
    TO: UUID | None = Field(default=None)
    category: UUID | None = Field(default=None)
    type: Literal['debit', 'adding', 'transfer'] | None = Field(default=None)
    debit_size: float = Field(alias="debitSize")
    credit_size: float | None = Field(default=None, alias="creditSize")
    exchange_rate: float | None = Field(default=None, alias="exchangeRate")
    date: datetime.date
    description: str | None
    split_type: Literal['equal', 'percentage', 'amount', 'position'] | None = Field(default=None, alias="splitType")
    status: Literal['pending', 'partially_paid', 'settled']
    related_transactions: UUID | None = Field(default=None, alias="relatedTransaction")
    distributions: list[distribution_in] | None = Field(default=None)


class transaction_in_type(BaseModel): #TODO убрать
    id: UUID
    FROM: UUID | None = None
    TO: UUID | None = None
    category: UUID | None = None
    type: str = Field(alias="type")


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
    category: UUID | None
    type: Literal['debit', 'adding', 'transfer'] | None
    debit_size: float | None = Field(serialization_alias='debitSize')
    credit_size: float | None = Field(serialization_alias='creditSize')
    exchange_rate: float | None = Field(serialization_alias='exchangeRate')
    date: datetime.date
    description: str | None
    split_type: Literal['equal', 'percentage', 'amount', 'position'] | None = Field(serialization_alias='splitType')
    status: Literal['pending', 'partially_paid', 'settled']
    related_transactions: UUID | None = Field(serialization_alias='relatedTransaction')
    transaction_distribution_user: list[distribution_out] = Field(min_length=1, serialization_alias='distributions')
