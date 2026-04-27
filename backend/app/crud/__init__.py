from sqlalchemy.orm import Session

from .crud_distribution import CRUD_distribution

from .crud_position import CRUD_position

from .crud_account import CRUD_account  
from .crud_category import CRUD_category  
from .crud_transaction import CRUD_transaction 
from .crud_user import CRUD_user 


class Crud:
    def __init__(self, db: Session, user_info: dict) -> None:
        self.account: CRUD_account = CRUD_account(db, user_info)
        self.category: CRUD_category = CRUD_category(db, user_info)
        self.transaction: CRUD_transaction = CRUD_transaction(db, user_info)
        self.distribution: CRUD_distribution = CRUD_distribution(db, user_info)
        self.position: CRUD_position = CRUD_position(db, user_info)
        self.user: CRUD_user = CRUD_user(db, user_info)
