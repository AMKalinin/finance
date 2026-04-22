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
    transaction_in_delete,
    transaction_in_description,
    transaction_in_size,
    transaction_in_type,
    distribution_in,
    position_in
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

        db_objects = [db_transaction]

        size = transaction_info.debit_size
        for distribution in transaction_info.distributions:
            if distribution.role == 'owner':
                size = distribution.size
                continue
            distribution.transaction_id = db_transaction.id
            db_objects.append(self.create_distribution(distribution))

        owner_distr_info = distribution_in(
                userId=self.user.id,
                transactionId=db_transaction.id,
                role='owner',size=size
        )
        print(db_transaction.id)
        db_objects.append(self.create_distribution(owner_distr_info))
        print(db_transaction.id)
        for position in transaction_info.positions:
            print(db_transaction.id)
            position.transaction_id = db_transaction.id
            db_objects.append(self.create_position(position))

        self.db.bulk_save_objects(db_objects)
        return db_transaction

    def create_distribution(self, distribution: distribution_in, save_to_db:bool=False) -> Transaction_distribution_user:
        db_distr = Transaction_distribution_user(
            user_id=distribution.user_id,
            transaction_id=distribution.transaction_id,
            distribution_user_role=distribution.role,
            size=distribution.size,
            distribution_status='settled'
        )
        if save_to_db:
            self.db.add(db_distr)
        return db_distr

    def create_position(self, position:position_in, save_to_db:bool=False) -> Position:
        print(position)
        db_position = Position(
                    name=position.name,
                    transaction_id=position.transaction_id,
                    price=position.price,
                    quantity=position.quantity
                )
        if save_to_db:
            self.db.add(db_position)
        return db_position

    def get_distribution(self, transaction_id:UUID) -> Transaction_distribution_user:
        res = [
            distr
            for distr in self.user.transaction_distribution_user
            if  distr.transaction_id == transaction_id
        ]
        return res[0]

    def get_positions(self, transaction_id:UUID) -> list[Position]:
        res = [
            position 
            for position in self.user.transaction_distribution_user
            if position.transaction_id == transaction_id
        ]
        return res

    def update_distribution(self, distribution_info:distribution_in) -> Transaction_distribution_user:
        db_distr = self.db.query(Transaction_distribution_user).get((distribution_info.user_id, distribution_info.transaction_id))
        if distribution_info.size:
            db_distr.size = distribution_info.size
        return db_distr

    def update_position(self, id:UUID, position_info:position_in) -> Position:
        db_position = self.db.query(Position).get(id)
        db_position.price = position_info.price
        db_position.quantity = position_info.quantity

        return db_position 

    def delete_distribution(self, distribution_info:distribution_in) -> None:
        db_distr = self.db.query(Transaction_distribution_user).get((distribution_info.user_id, distribution_info.transaction_id))
        self.db.delete(db_distr)
 
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
