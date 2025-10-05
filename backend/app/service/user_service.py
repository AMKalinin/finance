from uuid import UUID
from sqlalchemy.orm import  Session

from app.crud import Crud
from app.core.utils import commit



class User_service:
    def __init__(self, db: Session, user_info: dict) -> None:
        self.db: Session = db
        self.crud: Crud = Crud(self.db, user_info)
        self.user_info: dict = user_info

    
    def get_user_info(self):
        return self.crud.user.get_info()

    def get_friends(self):
        return self.crud.user.get_friedns()

    @commit
    def add_friend(self, friends_user_id:UUID):
        return self.crud.user.add_friend(friends_user_id)

    @commit
    def accept_friend(self, friends_user_id:UUID):
        return self.crud.user.accept_friend(friends_user_id)

    @commit
    def reject_friend(self, friends_user_id:UUID):
        return self.crud.user.reject_friend(friends_user_id)

    @commit
    def delete_friend(self, friends_user_id:UUID):
        return self.crud.user.delete_friend(friends_user_id)

    @commit
    def set_subscription_type(self, user_in_subscription): 
        return self.crud.user.update_subscription_info(user_in_subscription)
