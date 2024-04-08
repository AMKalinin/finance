import datetime
from uuid import UUID

from pydantic import BaseModel


class transaction_in(BaseModel):
    FROM: UUID | None
    TO: UUID | None
    size: float
    data: datetime.datetime
    category: int | None
    type: int
    description: str


class transaction_in_type(BaseModel):
    id: UUID
    FROM: UUID | None
    TO: UUID | None
    category: int | None
    type: int


class transaction_in_size(BaseModel):
    id: UUID
    size: int


class transaction_in_data(BaseModel):
    id: UUID
    data: datetime.datetime


class transaction_in_category(BaseModel):
    id: UUID
    category: int


class transaction_in_description(BaseModel):
    id: UUID
    description: str


class transaction_out(BaseModel):
    id: UUID
    FROM: UUID | None
    TO: UUID | None
    size: float
    data: datetime.datetime
    category: int | None
    type: int
    description: str
