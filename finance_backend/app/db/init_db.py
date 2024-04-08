from sqlalchemy.orm import Session  # noqa

from app.models.accaunt import Accaunt  # noqa
from app.models.category import Category  # noqa
from app.models.transaction import Transaction  # noqa
from app.models.type import Type  # noqa

from .base_class import Base
from .session import engine


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
