from datetime import date

from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.type_transaction import Type_transaction  # noqa
from app.schemas.transaction import (
    transaction_in,
    transaction_in_date,
    transaction_in_description,
    transaction_in_size,
    transaction_in_type,
)


class CRUD_transaction:
    def create_transaction(self, db: Session, transaction_info: transaction_in) -> Transaction:
        db_FROM = db.query(Account).filter(Account.id == transaction_info.FROM).one()
        db_TO = db.query(Account).filter(Account.id == transaction_info.TO).one()

        db_category = db.query(Category).filter(Category.id == transaction_info.category).first()

        db_type = (
            db.query(Type_transaction)
            .filter(Type_transaction.name == transaction_info.type_name)
            .one()
        )

        match db_type.name:
            case "Debit":
                FROM_id = db_FROM.id
                TO_id = None
                category_id = db_category.id
            case "Transfer":
                FROM_id = db_FROM.id
                TO_id = db_TO.id
                category_id = None
            case "Adding":
                FROM_id = None
                TO_id = db_TO.id
                category_id = db_category.id

        db_transaction = Transaction(
            FROM=FROM_id,
            TO=TO_id,
            size=transaction_info.size,
            date=transaction_info.date,
            category=category_id,
            type_name=db_type.name,
            description=transaction_info.description,
        )  # type: ignore
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)

        return db_transaction

    def get_all_transaction(self, db: Session) -> list[Transaction]:
        return db.query(Transaction).all()

    def get_all_transaction_by_type(self, db: Session, type_name: str) -> list[Transaction]:
        return db.query(Transaction).filter(Transaction.type_name == type_name).all()

    def get_all_transaction_for_period(
        self, db: Session, from_date: date, to_date: date
    ) -> list[Transaction]:

        res = (
            db.query(Transaction)
            .filter(Transaction.date >= from_date)
            .filter(Transaction.date <= to_date)
            .all()
        )
        return res

    def get_all_transaction_for_period_with_type(
        self, db: Session, from_date: date, to_date: date, type_name: str
    ) -> list[Transaction]:

        res = (
            db.query(Transaction)
            .filter(Transaction.date >= from_date)
            .filter(Transaction.date <= to_date)
            .filter(Transaction.type_name == type_name)
            .all()
        )
        return res

    def update_type(self, db: Session, transaction_info: transaction_in_type) -> Transaction:
        db_transaction = db.query(Transaction).get(transaction_info.id)
        db_transaction.type_name = transaction_info.type_name
        db_transaction.FROM = transaction_info.FROM
        db_transaction.TO = transaction_info.TO
        db_transaction.category = transaction_info.category
        db.commit()
        return db_transaction

    def update_size(self, db: Session, transaction_info: transaction_in_size) -> Transaction:
        db_transaction = db.query(Transaction).get(transaction_info.id)
        db_transaction.size = transaction_info.size
        db.commit()
        return db_transaction

    def update_date(self, db: Session, transaction_info: transaction_in_date) -> Transaction:
        db_transaction = db.query(Transaction).get(transaction_info.id)
        db_transaction.date = transaction_info.date
        db.commit()
        return db_transaction

    def update_description(
        self, db: Session, transaction_info: transaction_in_description
    ) -> Transaction:
        db_transaction = db.query(Transaction).get(transaction_info.id)
        db_transaction.description = transaction_info.description
        db.commit()
        return db_transaction

    def delete_transaction(self, db: Session):
        pass


transaction = CRUD_transaction()
