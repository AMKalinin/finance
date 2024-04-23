from sqlalchemy.orm import Session

from app import crud


def get_all_currency(db: Session):
    pass


def create_currency_pair(db: Session) -> list[tuple[str, str]]:
    pairs = []
    currency = crud.currency.get_all(db)

    for cur in currency:
        if cur.name != "USD":
            pairs.append(("USD", cur.name))

    return pairs


def get_exchange_rate(pairs: list[tuple[str, str]]) -> dict[tuple[str, str], float]:

    return {}


def write_rate(db: Session):
    pass
