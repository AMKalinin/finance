from uuid import UUID
from app.crud.crud_base import CRUD_base
from app.err.errors import AcceptFriendError
from app.models.user import User
from app.models.friends import Friends

class CRUD_user(CRUD_base):
    def get_info(self):
        return self.user

    def update_subscription_info(self, user_in_subscription):
        self.user.subscription_type = user_in_subscription.type
        self.user.subscription_expiry = user_in_subscription.date
        return self.user

    def get_friedns(self):
        friends = self.user.friends
        return friends

    def add_friend(self, user_id:UUID):
        friend_1 = Friends(
                user1_id = self.user.id,
                user2_id = user_id,
                status = 'pending_sent'
                )
        friend_2 = Friends(
                user1_id = user_id,
                user2_id = self.user.id,
                status = 'pending_received'
                )
        self.db.add(friend_1)
        self.db.add(friend_2)
        return friend_1, friend_2

    def accept_friend(self, friend_id:UUID):
        friend_1 = self.db.query(Friends).get((self.user.id, friend_id))
        if friend_1.status != 'pending_received':
            raise AcceptFriendError('Вы не можете подтвердить дружбу') 
        friend_2 = self.db.query(Friends).get((friend_id, self.user.id ))
        
        friend_1.status = 'accept'
        friend_2.status = 'accept'
        return friend_1, friend_2
    
    def reject_friend(self, friend_id:UUID):
        friend_1 = self.db.query(Friends).get((self.user.id, friend_id))
        if friend_1.status != 'pending_received':
            raise AcceptFriendError('Вы не можете отклонить дружбу')
        friend_2 = self.db.query(Friends).get((friend_id, self.user.id ))
        self.db.delete(friend_1)
        self.db.delete(friend_2) 

    def delete_friend(self, friend_id:UUID):
        friend_1 = self.db.query(Friends).get((self.user.id, friend_id))
        friend_2 = self.db.query(Friends).get((friend_id, self.user.id ))
        self.db.delete(friend_1)
        self.db.delete(friend_2)

