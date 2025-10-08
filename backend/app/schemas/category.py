from uuid import UUID
from pydantic import BaseModel, Field


class category_in(BaseModel):
    name: str
    type: str = Field( default=None)
    parent_category: UUID | None = Field(alias="parentCategory",
                                         default=None)
    level: int | None = 1


class category_in_name(BaseModel):
    id: UUID
    name: str


class category_out(BaseModel):
    id: UUID
    name: str
    type: str
    level:int
    children: list['category_out'] = Field(default=[], serialization_alias="subCategory")
