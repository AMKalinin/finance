from uuid import UUID
from typing import Literal
from pydantic import BaseModel, Field


class distribution_in(BaseModel):
    model_config = {'populate_by_name': True}

    user_id: UUID | None = Field(default=None, alias='userId')
    transaction_id: UUID | None = Field(default=None, alias='transactionId')
    role: Literal['owner', 'participant'] = Field(default='participant', alias='role')
    size: float | None = Field(default=None)
    percentage: float | None = Field(default=None)


class distribution_out(BaseModel):
    user_id: UUID = Field(serialization_alias='userId')
    transaction_id: UUID = Field(serialization_alias='transactionId')
    distribution_user_role: Literal['owner', 'participant'] = Field(serialization_alias='role')
    distribution_status: Literal['pending', 'settled'] = Field(serialization_alias='status')
    size: float | None = Field(default=None) 
    percentage: float | None = Field(default=None)
    is_deleted: bool = False

    class Config:
        from_attributes = True


class distribution_settle_in(BaseModel):
    model_config = {'populate_by_name': True}

    user_id: UUID = Field(alias='userId')
    transaction_id: UUID = Field(alias='transactionId')
