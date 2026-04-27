from datetime import date
from uuid import UUID

from app.crud.crud_base import CRUD_base
from app.models.transaction import Transaction
from app.models.transaction_distribution_user import Transaction_distribution_user 
from app.models.position import Position

# from app.models.type_transaction import Type_transaction  # noqa
from app.schemas.transaction import (
    transaction_in,
    transaction_in_date,
    transaction_in_description,
    transaction_in_size,
)


class CRUD_transaction(CRUD_base):
    def create_transaction(self, transaction_info: transaction_in) -> Transaction:
        db_transaction = Transaction(
            from_account_id=transaction_info.FROM,
            to_account_id=transaction_info.TO,
            category=transaction_info.category,
            type=transaction_info.type,
            debit_size=transaction_info.debit_size,
            credit_size=transaction_info.credit_size,
            exchange_rate=transaction_info.exchange_rate,
            date=transaction_info.date,
            split_type=transaction_info.split_type,
            status=transaction_info.status,
            #related_transactions=transaction_info.related_transactions,
            description=transaction_info.description
        )  # type: ignore 
        self.db.add(db_transaction)
        self.db.flush()
 
        return db_transaction

    def get_by_id(self, id: UUID) -> Transaction:
        res = [
            distr.transactions 
            for distr in self.user.transaction_distribution_user
            if  distr.transaction_id == id
        ]
        return res[0]

    def get_all_transaction(self) -> list[Transaction]:
        return [distr.transactions for distr in self.user.transaction_distribution_user]

    def get_all_transaction_for_period(self, from_date: date, to_date: date) -> list[Transaction]:
        res = [
            distr.transactions 
            for distr in self.user.transaction_distribution_user
            if from_date <= distr.transactions.date <= to_date
        ]
        return res

    def get_all_transaction_for_period_with_type(
        self, from_date: date, to_date: date, type_name: str
    ) -> list[Transaction]:
        res = [
            distr.transactions 
            for distr in self.user.transaction_distribution_user
            if from_date <= distr.transactions.date <= to_date and distr.transactions.type == type_name
        ]
        return res
 
    def update_size(self, transaction_info: transaction_in_size) -> Transaction:
        db_transaction = self.db.query(Transaction).get(transaction_info.id)

        if db_transaction == None:
            return db_transaction

        db_transaction.size = transaction_info.size
        return db_transaction

    def update_date(self, transaction_info: transaction_in_date) -> Transaction:
        db_transaction = self.db.query(Transaction).get(transaction_info.id)
        if db_transaction == None:
            return db_transaction

        db_transaction.date = transaction_info.date
        return db_transaction

    def update_description(self, transaction_info: transaction_in_description) -> Transaction:
        db_transaction = self.db.query(Transaction).get(transaction_info.id)
        if db_transaction == None:
            return db_transaction

        db_transaction.description = transaction_info.description
        return db_transaction

    def delete(self, id: UUID) -> Transaction:
        db_transaction = self.db.query(Transaction).get(id)
        self.db.delete(db_transaction)
        return db_transaction
