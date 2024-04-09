from uuid import UUID

from sqlalchemy.orm import Session

from app.models.account import Account
from app.schemas.account import (
    account_in,
    account_in_balance,
    account_in_description,
    account_in_name,
)


class CRUD_account:
    def get_all(self, db: Session) -> list[Account]:
        return db.query(Account).all()

    def create_account(self, db: Session, account_info: account_in) -> Account:
        db_account = Account(
            balance=account_info.balance,
            name=account_info.name,
            description=account_info.description,
        )  # type: ignore
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account

    def get_by_id(self, db: Session, id: UUID) -> Account:
        return db.query(Account).get(id)

    def update_balance(self, db: Session, account_info: account_in_balance) -> Account:
        db_account = db.query(Account).get(account_info.id)

        if account_info.operation == "minus":
            db_account.balance -= account_info.balance
        elif account_info.operation == "plus":
            db_account.balance += account_info.balance
        elif account_info.operation == "update":
            db_account.balance = account_info.balance

        db.commit()
        return db_account

    def update_name(self, db: Session, account_info: account_in_name) -> Account:
        db_account = db.query(Account).get(account_info.id)
        db_account.name = account_info.name
        db.commit()
        return db_account

    def update_description(self, db: Session, account_info: account_in_description) -> Account:
        db_account = db.query(Account).get(account_info.id)
        db_account.description = account_info.description
        db.commit()
        return db_account

    def delete_account(self):
        pass


account = CRUD_account()
