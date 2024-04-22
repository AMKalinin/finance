from sqlalchemy.orm import Session

from app.models.currency import Currency


class CRUD_currency:
    def get_all(self, db: Session) -> list[Currency]:
        return db.query(Currency).all()

    def create_currency(self, db: Session, currency_info) -> Currency:
        db_currency = Currency(
            name=currency_info.name,
        )  # type: ignore
        db.add(db_currency)
        db.commit()
        db.refresh(db_currency)
        return db_currency


currency = CRUD_currency()
