from sqlalchemy.orm import Session

# from app.models.accaunt import Accaunt
# from app.models.category import Category
from app.models.type import Type

from .base_class import Base
from .session import engine

# import datetime


# from app.models.transaction import Transaction


def init_db():
    Base.metadata.create_all(engine)  # type: ignore

    with Session(engine) as session:
        with session.begin():
            type_debit = session.query(Type).filter(Type.name == "debit").first()
            if not type_debit:
                type_debit = Type(name="debit", description="debit списание")  # type: ignore

                session.add(type_debit)
