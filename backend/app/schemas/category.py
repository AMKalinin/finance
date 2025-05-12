from pydantic import BaseModel, Field


class category_in(BaseModel):
    name: str
    type_category: str = Field(alias="typeCategory")


class category_in_name(BaseModel):
    id: int
    name: str


class category_out(BaseModel):
    id: int
    name: str
    type_category: str = Field(serialization_alias="typeCategory")
