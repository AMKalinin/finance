from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict



class position_split_in(BaseModel):
    user_id: UUID | None = Field(default=None, alias='userId')
    transaction_id: UUID | None = Field(default=None, alias='transactionId')
    quantity: int | None = Field(default=None)


class position_in(BaseModel):
    name: str
    transaction_id: UUID | None = Field(default=None, alias='transactionId')
    price: float
    quantity: float


class position_out(BaseModel):
    id:UUID
    name: str
    transaction_id: UUID = Field(serialization_alias='transactionId')
    price: float
    quantity: float
    model_config = ConfigDict(from_attributes=True)


