from sqlalchemy.orm import Session

from app.models.accaunt import Accaunt
from app.models.category import Category
from app.models.transaction import Transaction
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

                type_perevod = Type(name="perevod", description="perevod перевод")  # type: ignore
                session.add(type_perevod)

                type_popolnenie = Type(name="popolnenie", description="пополнение")  # type: ignore
                session.add(type_popolnenie)

        with session.begin():
            acc1 = Accaunt(name="Дебитовая карта", description="основаная карта")  # type: ignore
            acc2 = Accaunt(name="Топливная карта", description="топливная карта")  # type: ignore

            session.add(acc1)
            session.add(acc2)

        with session.begin():
            cat1 = Category(name="products")  # type: ignore
            cat2 = Category(name="ЗП")  # type: ignore

            session.add(cat1)
            session.add(cat2)

        with session.begin():
            transaction1 = Transaction(
                FROM=acc1.id,
                TO=acc2.id,
                size=100,
                category=None,
                type=type_perevod.id,
                description="перевод",
            )  # type: ignore

            transaction2 = Transaction(
                FROM=None,
                TO=acc1.id,
                size=123,
                category=cat2.id,
                type=type_popolnenie.id,
                description="пополнение",
            )  # type: ignore

            transaction3 = Transaction(
                FROM=acc1.id,
                TO=None,
                size=50,
                category=cat1.id,
                type=type_debit.id,
                description="Списание",
            )  # type: ignore

            session.add(transaction1)
            session.add(transaction2)
            session.add(transaction3)
