import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class transaction_in(BaseModel):
    FROM: UUID | None
    TO: UUID | None
    size: float
    date: datetime.datetime
    category: int | None
    type_name: str = Field(alias="typeName")
    description: str


class transaction_in_type(BaseModel):
    id: UUID
    FROM: UUID | None
    TO: UUID | None
    category: int | None
    type_name: str = Field(alias="typeName")


class transaction_in_size(BaseModel):
    id: UUID
    size: int


class transaction_in_data(BaseModel):
    id: UUID
    date: datetime.datetime


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
    date: datetime.datetime
    category: int | None
    type_name: str = Field(serialization_alias="typeName")
    description: str