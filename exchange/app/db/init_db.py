from sqlalchemy.orm import Session  # noqa

from app.models.currency import Currency  # noqa
from app.models.exchange_rate import Exchange_rate  # noqa

from .base_class import Base
from .session import engine


def init_db():
    Base.metadata.create_all(engine)  # type: ignore

    with Session(engine) as session:
        with session.begin():
            usd = session.query(Currency).filter(Currency.name == "USD").first()
            if not usd:
                usd = Currency(name="USD")  # type: ignore
                session.add(usd)

                rub = Currency(name="RUB")  # type: ignore
                session.add(rub)
