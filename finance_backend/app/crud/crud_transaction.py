from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.type_transaction import Type_transaction  # noqa
from app.schemas.transaction import transaction_in


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

    def get_all_transaction_for_period(self):
        pass

    def delete_transaction(self):
        pass

    def update_type(self):
        pass

    def update_size(self):
        pass

    def update_date(self):
        pass

    def update_description(self):
        pass


transaction = CRUD_transaction()
