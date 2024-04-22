from sqlalchemy.orm import Session

from app.models.exchange_rate import Exchange_rate
from app.schemas.exchange import exchange


class CRUD_exchange:
    def get_all(self, db: Session) -> list[Exchange_rate]:
        return db.query(Exchange_rate).all()

    def create_exchange(self, db: Session, ex_rate_info: exchange) -> Exchange_rate:
        db_ex_rate = Exchange_rate(
            from_currency_name=ex_rate_info.from_currancy,
            to_currency_name=ex_rate_info.to_currancy,
            rate=ex_rate_info.rate,
            timestamp=ex_rate_info.timestamp,
        )  # type: ignore
        db.add(db_ex_rate)
        db.commit()
        db.refresh(db_ex_rate)
        return db_ex_rate

    def get_last_exchange_rate(
        self, db: Session, from_cur: str, to_cur: str
    ) -> Exchange_rate | None:

        rate = (
            db.query(Exchange_rate)
            .filter(Exchange_rate.from_currency_name == from_cur)
            .filter(Exchange_rate.to_currency_name == to_cur)
            .order_by(Exchange_rate.timestamp)
            .first()
        )
        return rate


ex_rate = CRUD_exchange()
