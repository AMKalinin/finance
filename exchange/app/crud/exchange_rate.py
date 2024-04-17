from sqlalchemy.orm import Session

from app.models.exchange_rate import Exchange_rate


class CRUD_exchange:
    def get_all(self, db: Session) -> list[Exchange_rate]:
        return db.query(Exchange_rate).all()

    def create_exchange(self, db: Session, ex_rate_info) -> Exchange_rate:
        db_ex_rate = Exchange_rate(
            name=ex_rate_info.name,
        )  # type: ignore
        db.add(db_ex_rate)
        db.commit()
        db.refresh(db_ex_rate)
        return db_ex_rate
