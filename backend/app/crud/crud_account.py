from uuid import UUID

from app.crud.crud_base import CRUD_base
from app.models.account import Account
from app.schemas.account import (
    account_in,
    account_in_balance,
    account_in_description,
    account_in_name,
    account_in_interest_rate,
    account_in_archived,
    account_in_decimal_places,
    account_in_emergency_fund,
    account_in_primary
)


class CRUD_account(CRUD_base):
    def get_all(self) -> list[Account]:
        return self.user.accounts.filter(Account.is_deleted == False).all()  # self.db.query(Account).all()

    def create_account(self, account_info: account_in) -> Account:
        db_account = Account(
            balance=account_info.balance,
            currency=account_info.currency,
            name=account_info.name,
            description=account_info.description,
            interest_rate=account_info.interest_rate,
            is_emergency_fund=account_info.is_emergency_fund,
            decimal_places=account_info.decimal_places,
            is_archived=account_info.is_archived,
            is_primary=account_info.is_primary,
            account_type=account_info.account_type,
            user_id=self.user.id,
        )  # type: ignore
        self.db.add(db_account)
        return db_account

    def get_by_id(self, id: UUID) -> Account:
        return self.user.accounts.filter(Account.id == id).first()  # self.db.query(Account).get(id)

    def update_balance(self, account_info: account_in_balance) -> Account:
        db_account = self.user.accounts.filter(
            Account.id == account_info.id
        ).first()  # self.db.query(Account).get(account_info.id)

        if db_account == None:
            return db_account

        if account_info.operation == "minus":
            db_account.balance -= account_info.balance
        elif account_info.operation == "plus":
            db_account.balance += account_info.balance
        elif account_info.operation == "update":
            db_account.balance = account_info.balance

        return db_account

    def update_name(self, account_info: account_in_name) -> Account:
        db_account = self.user.accounts.filter(
            Account.id == account_info.id
        ).first()  # self.db.query(Account).get(account_info.id)

        if db_account == None:
            return db_account

        db_account.name = account_info.name
        return db_account

    def update_description(self, account_info: account_in_description) -> Account:
        db_account = self.user.accounts.filter(
            Account.id == account_info.id
        ).first()  # self.db.query(Account).get(account_info.id)

        if db_account == None:
            return db_account

        db_account.description = account_info.description
        return db_account

    def update_interest_rate(self, account_info: account_in_interest_rate) -> Account:
        db_account = self.user.accounts.filter(
            Account.id == account_info.id
        ).first()  # self.db.query(Account).get(account_info.id)

        if db_account == None:
            return db_account

        db_account.interest_rate = account_info.interest_rate
        return db_account
    
    def update_emergency_fund(self, account_info: account_in_emergency_fund) -> Account:
        db_account = self.user.accounts.filter(
            Account.id == account_info.id
        ).first()  # self.db.query(Account).get(account_info.id)

        if db_account == None:
            return db_account

        db_account.is_emergency_fund = account_info.is_emergency_fund
        return db_account

    def update_decimal_places(self, account_info: account_in_decimal_places) -> Account:
        db_account = self.user.accounts.filter(
            Account.id == account_info.id
        ).first()  # self.db.query(Account).get(account_info.id)

        if db_account == None:
            return db_account

        db_account.decimal_places = account_info.decimal_places
        return db_account

    def update_archived(self, account_info: account_in_archived) -> Account:
        db_account = self.user.accounts.filter(
            Account.id == account_info.id
        ).first()  # self.db.query(Account).get(account_info.id)

        if db_account == None:
            return db_account

        db_account.is_archived = account_info.is_archived
        return db_account

    def update_primary(self, account_info: account_in_primary) -> Account:
        db_account = self.user.accounts.filter(
            Account.id == account_info.id
        ).first()  # self.db.query(Account).get(account_info.id)

        if db_account == None:
            return db_account

        db_account.is_primary = account_info.is_primary
        return db_account

    def delete(self, id: UUID) -> Account:
        db_account = self.user.accounts.filter(
            Account.id == id
        ).first()  # self.db.query(Account).get(account_info.id)

        if db_account == None:
            return db_account

        db_account.is_deleted = True
        return db_account


# account = CRUD_account()
