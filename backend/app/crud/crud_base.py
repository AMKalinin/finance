from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User


class CRUD_base:
    def __init__(self, db: Session, user_info: dict) -> None:
        self.db: Session = db
        self.user: User = self.create_or_get_user(user_info)

    def commit(self):
        self.db.commit()

    def create_or_get_user(self, user_info: dict) -> User:
        uid = UUID(user_info["sub"])
        user = self.db.query(User).get(uid)
        if user == None:
            user = User(id=uid, description="v1")
            self.db.add(user)
            self.commit()
        return user
