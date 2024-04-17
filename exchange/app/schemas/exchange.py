from pydantic import BaseModel
from datetime import datetime


class exchange_in(BaseModel):
    from_currancy: str
    to_currancy: str
    rate: float
    timestamp: datetime
