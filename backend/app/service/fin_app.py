from datetime import date
from uuid import UUID

from sqlalchemy.orm import PassiveFlag, Session

from app.crud import Crud
from app.models.account import Account
from app.schemas.account import (
    account_in,
    account_in_balance,
    account_in_description,
    account_in_name,
)
from app.schemas.category import category_in, category_in_name
from app.schemas.transaction import (
    transaction_in,
    transaction_in_date,
    transaction_in_delete,
    transaction_in_description,
    transaction_in_size,
    transaction_in_type,
)


def commit(func):
    def wrapper(self, *args, **kwargs):
        flag = True
        if "commit_transaction" in kwargs:
            flag = kwargs["commit_transaction"]
            kwargs.pop("commit_transaction")
        res = func(self, *args, **kwargs)
        if flag:
            self.db.commit()
        # self.db.refresh(res)
        return res

    return wrapper


class Fin_app:
    def __init__(self, db: Session, user_info: dict) -> None:
        self.db: Session = db
        self.crud: Crud = Crud(self.db, user_info)

    @commit
    def create_account(self, account_info: account_in) -> Account:
        acc = self.crud.account.create_account(account_info)
        return acc

    def get_all_account(self) -> list[Account]:
        acc_list = self.crud.account.get_all()
        return acc_list

    def get_account_by_id(self, id: UUID) -> Account:
        acc = self.crud.account.get_by_id(id)
        return acc

    @commit
    def update_account_balance(self, account_info: account_in_balance) -> Account:
        acc = self.crud.account.update_balance(account_info)
        return acc

    @commit
    def update_account_name(self, account_info: account_in_name) -> Account:
        acc = self.crud.account.update_name(account_info)
        return acc

    @commit
    def update_account_description(self, account_info: account_in_description) -> Account:
        acc = self.crud.account.update_description(account_info)
        return acc

    def delete_account(self):
        pass

    def get_all_category(self):
        return self.crud.category.get_all()

    @commit
    def create_category(self, category_info: category_in):
        category = self.crud.category.create_category(category_info)
        return category

    def delete_category(self):
        pass

    @commit
    def update_category(self, category_info: category_in_name):
        category = self.crud.category.update_name(category_info)
        return category

    def get_all_transaction(self):
        return self.crud.transaction.get_all_transaction()

    def get_all_transaction_by_type(self, operation_type: str):
        return self.crud.transaction.get_all_transaction_by_type(operation_type)

    def get_all_transaction_for_period(self, from_date: date, to_date: date):
        return self.crud.transaction.get_all_transaction_for_period(from_date, to_date)

    def get_all_transaction_for_period_with_type(
        self, from_date: date, to_date: date, operation_type: str
    ):
        return self.crud.transaction.get_all_transaction_for_period_with_type(
            from_date, to_date, operation_type
        )

    @commit
    def create_transaction(self, transaction_info: transaction_in):
        # TODO скорее всего нужно вынести в отдельную функцию
        if transaction_info.type_name == "Debit":
            self.update_account_balance(
                account_in_balance(
                    id=transaction_info.FROM, operation="minus", balance=transaction_info.size
                ),
                commit_transaction=False,
            )
        elif transaction_info.type_name == "Transfer":
            self.update_account_balance(
                account_in_balance(
                    id=transaction_info.FROM, operation="minus", balance=transaction_info.size
                ),
                commit_transaction=False,
            )
            size = transaction_info.size * 1 # transaction_info.exchange_rate
            self.update_account_balance(
                account_in_balance(id=transaction_info.TO, operation="plus", balance=size),
                commit_transaction=False,
            )
        elif transaction_info.type_name == "Adding":
            self.update_account_balance(
                account_in_balance(
                    id=transaction_info.TO, operation="plus", balance=transaction_info.size
                ),
                commit_transaction=False,
            )

        db_from = self.crud.account.get_by_id(transaction_info.FROM)
        db_to = self.crud.account.get_by_id(transaction_info.TO)
        db_category = self.crud.category.get_by_id(transaction_info.category)

        match transaction_info.type_name:
            case "Debit":
                transaction_info.FROM = db_from.id
                transaction_info.TO = None
                transaction_info.category = db_category.id
            case "Transfer":
                transaction_info.FROM = db_from.id
                transaction_info.TO = db_to.id
                transaction_info.category = None
            case "Adding":
                transaction_info.FROM = None
                transaction_info.TO = db_to.id
                transaction_info.category = db_category.id

        transaction = self.crud.transaction.create_transaction(transaction_info)
        return transaction

    @commit
    def update_transaction_type(self, transaction_info: transaction_in_type):
        transaction = self.crud.transaction.update_type(transaction_info)
        return transaction

    @commit
    def update_transaction_date(self, transaction_info: transaction_in_date):
        transaction = self.crud.transaction.update_date(transaction_info)
        return transaction

    @commit
    def update_transaction_size(self, transaction_info: transaction_in_size):
        transaction = self.crud.transaction.update_size(transaction_info)
        return transaction

    @commit
    def update_transaction_description(self, transaction_info: transaction_in_description):
        return self.crud.transaction.update_description(transaction_info)

    @commit
    def delete_transaction(self, id: UUID):
        transaction = self.crud.transaction.delete(id)
        if transaction.type_name == "Debit":
            self.update_account_balance(
                account_in_balance(id=transaction.FROM, operation="plus", balance=transaction.size),
                commit_transaction=False,
            )
        elif transaction.type_name == "Transfer":
            self.update_account_balance(
                account_in_balance(id=transaction.FROM, operation="plus", balance=transaction.size),
                commit_transaction=False,
            )
            size = transaction.size * transaction.exchange_rate
            self.update_account_balance(
                account_in_balance(id=transaction.TO, operation="minus", balance=size),
                commit_transaction=False,
            )
        elif transaction.type_name == "Adding":
            self.update_account_balance(
                account_in_balance(id=transaction.TO, operation="minuse", balance=transaction.size),
                commit_transaction=False,
            )
        return transaction
