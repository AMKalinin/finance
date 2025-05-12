from sqlalchemy.orm import Session

from .crud_account import CRUD_account  # noqa
from .crud_category import CRUD_category  # noqa
from .crud_transaction import CRUD_transaction  # noqa


class Crud:
    def __init__(self, db: Session, user_info: dict) -> None:
        self.account: CRUD_account = CRUD_account(db, user_info)
        self.category: CRUD_category = CRUD_category(db, user_info)
        self.transaction: CRUD_transaction = CRUD_transaction(db, user_info)
