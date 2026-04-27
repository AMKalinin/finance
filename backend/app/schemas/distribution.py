from uuid import UUID
from typing import Literal
from pydantic import BaseModel, Field


class distribution_in(BaseModel):
    user_id: UUID | None = Field(default=None, alias='userId')
    transaction_id: UUID | None = Field(default=None, alias='transactionId')
    role: Literal['owner', 'participant'] = Field(default='participant')
    size: float | None = Field(default=None)


class distribution_out(BaseModel):
    user_id: UUID = Field(serialization_alias='userId')
    transaction_id: UUID = Field(serialization_alias='transactionId')
    distribution_user_role: Literal['owner', 'participant'] = Field(serialization_alias='role')
    size: float


