from datetime import date
from uuid import UUID

from app.crud.crud_base import CRUD_base
from app.models.transaction import Transaction
from app.models.transaction_distribution_user import Transaction_distribution_user 

# from app.models.type_transaction import Type_transaction  # noqa
from app.schemas.transaction import (
    transaction_in,
    transaction_in_date,
    transaction_in_delete,
    transaction_in_description,
    transaction_in_size,
    transaction_in_type,
    distribution_in,
)


class CRUD_transaction(CRUD_base):
    def create_transaction(self, transaction_info: transaction_in) -> Transaction:
        db_transaction = Transaction(
            FROM=transaction_info.FROM,
            TO=transaction_info.TO,
            category=transaction_info.category,
            type=transaction_info.type,
            debit_size=transaction_info.debit_size,
            credit_size=transaction_info.credit_size,
            exchange_rate=transaction_info.exchange_rate,
            date=transaction_info.date,
            split_type=transaction_info.split_type,
            status=transaction_info.status,
            related_transactions=transaction_info.related_transactions,
            description=transaction_info.description
        )  # type: ignore 
        self.db.add(db_transaction)
        self.db.flush()

        db_objects = [db_transaction]

        
        size = transaction_info.debit_size
        for distribution in transaction_info.distributions:
            if distribution.role == 'owner':
                size = distribution.size
                continue
            db_objects.append(self.create_distribution(distribution))

        owner_distr_info = distribution_in(
                userId=self.user.id,
                transactionId=db_transaction.id,
                role='owner',size=size
        )
        db_objects.append(self.create_distribution(owner_distr_info))
        
        self.db.bulk_save_objects(db_objects)
        return db_transaction

    def create_distribution(self, distribution: distribution_in, save_to_db:bool=False) -> Transaction_distribution_user:
        db_distr = Transaction_distribution_user(
            user_id=distribution.user_id,
            transaction_id=distribution.transaction_id,
            distribution_user_role=distribution.role,
            size=distribution.size
        )
        if save_to_db:
            self.db.add(db_distr)
        return db_distr

    def delete_distribution(self, distribution_info:distribution_in) -> None:
        db_distr = self.db.query(Transaction_distribution_user).get((distribution_info.user_id, distribution_info.transaction_id))
        self.db.delete(db_distr)

    def update_distribution_size(self, distribution_info:distribution_in) -> Transaction_distribution_user:
        db_distr = self.db.query(Transaction_distribution_user).get((distribution_info.user_id, distribution_info.transaction_id))
        db_distr.size = distribution_info.size
        return db_distr

    def get_by_id(self, id: UUID) -> Transaction:
        return self.user.transaction_distribution_user.filter(Transaction_distribution_user.transaction_id == id).first().transactions

    def get_all_transaction(self) -> list[Transaction]:
        return [distr.transactions for distr in self.user.transaction_distribution_user] #self.user.transactions.all()  # self.db.query(Transaction).all()

    def get_all_transaction_by_type(self, type_name: str) -> list[Transaction]:
        return self.user.transactions.filter(Transaction.type_name == type_name).all()

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

    def update_type(self, transaction_info: transaction_in_type) -> Transaction:
        db_transaction = self.db.query(Transaction).get(transaction_info.id)
        if db_transaction == None:
            return db_transaction

        db_transaction.type = transaction_info.type
        db_transaction.FROM = transaction_info.FROM
        db_transaction.TO = transaction_info.TO
        db_transaction.category = transaction_info.category

        return db_transaction

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
