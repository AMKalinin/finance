from pydantic import BaseModel, Field


class payment_in(BaseModel):
    order_id: str | None= Field(alias="orderId", default=None) 
    amount: float | None
    promo_code: str | None = Field(alias="promoCode", default=None)
