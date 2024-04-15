from sqlalchemy.orm import Session  # noqa

from app.models.account import Account  # noqa
from app.models.category import Category  # noqa
from app.models.transaction import Transaction  # noqa
from app.models.type_category import Type_category
from app.models.type_transaction import Type_transaction  # noqa

from .base_class import Base
from .session import engine


def init_db():
    Base.metadata.create_all(engine)  # type: ignore

    with Session(engine) as session:
        with session.begin():
            type_debit = (
                session.query(Type_transaction).filter(Type_transaction.name == "Debit").first()
            )
            if not type_debit:
                type_debit = Type_transaction(
                    name="Debit", description="Debit / списание"
                )  # type: ignore
                session.add(type_debit)

                type_transfer = Type_transaction(
                    name="Transfer", description="Transfer / перевод"
                )  # type: ignore
                session.add(type_transfer)

                type_adding = Type_transaction(
                    name="Adding", description="Adding / пополнение"
                )  # type: ignore
                session.add(type_adding)

                type_c_debit = Type_category(
                    name="Debit", description="Debit / списание"
                )  # type: ignore
                session.add(type_c_debit)

                type_c_adding = Type_category(
                    name="Adding", description="Adding / пополнение"
                )  # type: ignore
                session.add(type_c_adding)
