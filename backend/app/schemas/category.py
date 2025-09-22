from uuid import UUID
from pydantic import BaseModel, Field


class category_in(BaseModel):
    name: str
    type_category: str = Field(alias="typeCategory")
    parent_category: UUID | None = Field(alias="parentCategory")
    level: int


class category_in_name(BaseModel):
    id: UUID
    name: str


class category_out(BaseModel):
    id: UUID
    name: str
    type_category: str = Field(serialization_alias="typeCategory")
    is_active:bool = True
    sub_category: list['category_out'] = Field(default=[], serialization_alias="subCategory")
    level:int
