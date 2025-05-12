from datetime import date
from uuid import UUID

from app.crud.crud_base import CRUD_base
from app.models.transaction import Transaction

# from app.models.type_transaction import Type_transaction  # noqa
from app.schemas.transaction import (
    transaction_in,
    transaction_in_date,
    transaction_in_delete,
    transaction_in_description,
    transaction_in_size,
    transaction_in_type,
)


class CRUD_transaction(CRUD_base):
    def create_transaction(self, transaction_info: transaction_in) -> Transaction:
        db_transaction = Transaction(
            FROM=transaction_info.FROM,
            TO=transaction_info.TO,
            size=transaction_info.size,
            exchange_rate=transaction_info.exchange_rate,
            date=transaction_info.date,
            category=transaction_info.category,
            type_name=transaction_info.type_name,
            description=transaction_info.description,
            user_id=self.user.id,
        )  # type: ignore
        self.db.add(db_transaction)
        return db_transaction

    def get_by_id(self, id: UUID) -> Transaction:
        return self.user.transactions.filter(Transaction.id == id).first()

    def get_all_transaction(self) -> list[Transaction]:
        return self.user.transactions.all()  # self.db.query(Transaction).all()

    def get_all_transaction_by_type(self, type_name: str) -> list[Transaction]:
        return self.user.transactions.filter(Transaction.type_name == type_name).all()

    def get_all_transaction_for_period(self, from_date: date, to_date: date) -> list[Transaction]:

        res = (
            self.user.transactions.filter(Transaction.date >= from_date)
            .filter(Transaction.date <= to_date)
            .all()
        )
        return res

    def get_all_transaction_for_period_with_type(
        self, from_date: date, to_date: date, type_name: str
    ) -> list[Transaction]:

        res = (
            self.user.transactions.filter(Transaction.date >= from_date)
            .filter(Transaction.date <= to_date)
            .filter(Transaction.type_name == type_name)
            .all()
        )
        return res

    def update_type(self, transaction_info: transaction_in_type) -> Transaction:
        db_transaction = self.user.transactions.get(transaction_info.id)

        if db_transaction == None:
            return db_transaction

        db_transaction.type_name = transaction_info.type_name
        db_transaction.FROM = transaction_info.FROM
        db_transaction.TO = transaction_info.TO
        db_transaction.category = transaction_info.category

        return db_transaction

    def update_size(self, transaction_info: transaction_in_size) -> Transaction:
        db_transaction = self.user.transactions.get(transaction_info.id)

        if db_transaction == None:
            return db_transaction

        db_transaction.size = transaction_info.size
        return db_transaction

    def update_date(self, transaction_info: transaction_in_date) -> Transaction:
        db_transaction = self.user.transactions.get(transaction_info.id)

        if db_transaction == None:
            return db_transaction

        db_transaction.date = transaction_info.date
        return db_transaction

    def update_description(self, transaction_info: transaction_in_description) -> Transaction:
        db_transaction = self.user.transactions.get(transaction_info.id)

        if db_transaction == None:
            return db_transaction

        db_transaction.description = transaction_info.description
        return db_transaction

    def delete(self, id: UUID) -> Transaction:
        db_transaction = self.user.transactions.filter(Transaction.id == id).first()
        self.db.delete(db_transaction)
        return db_transaction
