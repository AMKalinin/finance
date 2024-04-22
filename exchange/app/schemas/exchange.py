from pydantic import BaseModel
from datetime import datetime


class exchange(BaseModel):
    from_currancy: str
    to_currancy: str
    rate: float
    timestamp: datetime
