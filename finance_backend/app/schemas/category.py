from pydantic import BaseModel


class category_in(BaseModel):
    name: str


class category_out(BaseModel):
    id: int
    name: str
