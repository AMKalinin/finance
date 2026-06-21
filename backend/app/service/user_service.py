"""
Сервис для работы с пользователем и друзьями.
"""

import logging
from uuid import UUID
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.friends import Friends
from app.err.errors import (
    UserNotFoundError,
    FriendNotFoundError,
    AlreadyFriendError,
    PendingRequestError,
    AcceptFriendError,
)
from app.logging_config import get_logger

logger = get_logger(__name__)

# Валидные статусы из таблицы friends_status
STATUS_PENDING_SENT = "pending_sent"
STATUS_PENDING_RECEIVED = "pending_received"
STATUS_ACCEPT = "accept"

class User_service:
    """Сервис для работы с пользователями и друзьями."""

    def __init__(self, db: Session, user_info: dict):
        self.db = db
        self.user_id = UUID(user_info["sub"]) if "sub" in user_info else None
        logger.info(f"User service initialized for user {self.user_id}")

    def _ensure_user_exists(self, user_id: UUID) -> User:
        """Убедиться, что пользователь существует в БД. Если нет — создать."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id, description="", subscription_type="free")
            self.db.add(user)
            self.db.flush()
        return user

    def get_user_info(self) -> dict:
        """Получить информацию о пользователе."""
        try:
            user = self._ensure_user_exists(self.user_id)
            return {
                "id": str(user.id),
                "description": user.description or "",
                "subscription_type": user.subscription_type,
                "subscription_expiry": user.subscription_expiry.isoformat() if user.subscription_expiry else None,
                "friends_count": len(user.friends),
            }
        except Exception as e:
            logger.error(f"Error getting user info: {e}", exc_info=True)
            raise

    def _get_initials(self, name: Optional[str]) -> str:
        """Получить инициалы из имени."""
        if not name:
            return "??"
        parts = name.strip().split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        elif len(name) >= 2:
            return name[:2].upper()
        return name.upper()

    def get_friends(self) -> List[dict]:
        """Получить список друзей."""
        try:
            friends = (
                self.db.query(Friends)
                .filter(Friends.user2_id == self.user_id, Friends.status == STATUS_ACCEPT)
                .all()
            )

            logger.info(f"User {self.user_id} has {len(friends)} friends")

            result = []
            for friend in friends:
                friend_user = friend.user1
                result.append(
                    {
                        "id": str(friend_user.id),
                        "name": friend_user.description or f"Пользователь {str(friend_user.id)[:8]}",
                        "initials": self._get_initials(friend_user.description),
                        "status": friend.status,
                        "created_at": friend.created_at.isoformat() if hasattr(friend, "created_at") and friend.created_at else None,
                    }
                )
            return result
        except Exception as e:
            logger.error(f"Error getting friends: {e}", exc_info=True)
            raise

    def get_friend_requests(self) -> List[dict]:
        """Получить запросы в дружбу (от других пользователей к нам, pending_received)."""
        try:
            requests = (
                self.db.query(Friends)
                .filter(
                    Friends.user2_id == self.user_id,
                    Friends.status == STATUS_PENDING_RECEIVED,
                )
                .all()
            )

            result = []
            for req in requests:
                requester = req.user1
                result.append(
                    {
                        "id": str(requester.id),
                        "name": requester.description or f"Пользователь {str(requester.id)[:8]}",
                        "initials": self._get_initials(requester.description),
                        "status": req.status,
                        "created_at": req.created_at.isoformat() if hasattr(req, "created_at") and req.created_at else None,
                    }
                )
            return result
        except Exception as e:
            logger.error(f"Error getting friend requests: {e}", exc_info=True)
            raise

    def get_sent_requests(self) -> List[dict]:
        """Получить отправленные запросы в дружбу (pending_sent)."""
        try:
            sent = (
                self.db.query(Friends)
                .filter(
                    Friends.user1_id == self.user_id,
                    Friends.status == STATUS_PENDING_SENT,
                )
                .all()
            )

            result = []
            for req in sent:
                recipient = req.user2
                result.append(
                    {
                        "id": str(recipient.id),
                        "name": recipient.description or f"Пользователь {str(recipient.id)[:8]}",
                        "initials": self._get_initials(recipient.description),
                        "status": req.status,
                        "created_at": req.created_at.isoformat() if hasattr(req, "created_at") and req.created_at else None,
                    }
                )
            return result
        except Exception as e:
            logger.error(f"Error getting sent requests: {e}", exc_info=True)
            raise

    def add_friend(self, friend_id: UUID) -> dict:
        """Добавить друга (отправить запрос)."""
        try:
            friend = self._ensure_user_exists(friend_id)

            # Проверяем любые существующие связи между пользователями
            existing = (
                self.db.query(Friends)
                .filter(
                    ((Friends.user1_id == friend_id) & (Friends.user2_id == self.user_id))
                    | ((Friends.user1_id == self.user_id) & (Friends.user2_id == friend_id))
                )
                .first()
            )

            if existing:
                raise AlreadyFriendError(str(friend_id))

            # Создаём два record'а:
            # 1. user1=friend_id, user2=self.user_id, status=pending_received (для получателя)
            # 2. user1=self.user_id, user2=friend_id, status=pending_sent (для отправителя)
            new_friendship = Friends(
                user1_id=friend_id,
                user2_id=self.user_id,
                status=STATUS_PENDING_RECEIVED,
            )
            self.db.add(new_friendship)

            reverse_friendship = Friends(
                user1_id=self.user_id,
                user2_id=friend_id,
                status=STATUS_PENDING_SENT,
            )
            self.db.add(reverse_friendship)
            self.db.commit()

            logger.info(f"Friend request sent from {self.user_id} to {friend_id}")

            return {
                "id": f"{new_friendship.user1_id}|{new_friendship.user2_id}",
                "user1_id": str(new_friendship.user1_id),
                "user2_id": str(new_friendship.user2_id),
                "status": new_friendship.status,
                "message": f"Запрос в дружбе отправлен пользователю {friend_id}",
            }
        except (AlreadyFriendError, PendingRequestError):
            raise
        except Exception as e:
            logger.error(f"Error adding friend {friend_id}: {e}", exc_info=True)
            self.db.rollback()
            raise AcceptFriendError(f"Ошибка при отправке запроса в друзья: {str(e)}")

    def accept_friend(self, friend_id: UUID) -> dict:
        """Принять запрос в дружбу."""
        try:
            pending_request = (
                self.db.query(Friends)
                .filter(
                    Friends.user1_id == friend_id,
                    Friends.user2_id == self.user_id,
                    Friends.status == STATUS_PENDING_RECEIVED,
                )
                .first()
            )

            if not pending_request:
                raise PendingRequestError(str(friend_id))

            pending_request.status = STATUS_ACCEPT
            self.db.commit()

            logger.info(f"Friend request from {friend_id} accepted by {self.user_id}")

            return {
                "id": f"{pending_request.user1_id}|{pending_request.user2_id}",
                "user1_id": str(pending_request.user1_id),
                "user2_id": str(pending_request.user2_id),
                "status": pending_request.status,
                "message": f"Дружба подтверждена с пользователем {friend_id}",
            }
        except (PendingRequestError, AcceptFriendError):
            raise
        except Exception as e:
            logger.error(f"Error accepting friend request from {friend_id}: {e}", exc_info=True)
            self.db.rollback()
            raise

    def reject_friend(self, friend_id: UUID) -> dict:
        """Отклонить входящий запрос в дружбу."""
        try:
            pending_request = (
                self.db.query(Friends)
                .filter(
                    Friends.user1_id == friend_id,
                    Friends.user2_id == self.user_id,
                    Friends.status == STATUS_PENDING_RECEIVED,
                )
                .first()
            )

            if not pending_request:
                raise PendingRequestError(str(friend_id))

            self.db.delete(pending_request)
            self.db.commit()

            logger.info(f"Friend request from {friend_id} rejected by {self.user_id}")

            return {"message": f"Запрос в дружбе отклонен пользователю {friend_id}", "status": "rejected"}
        except (PendingRequestError, AcceptFriendError):
            raise
        except Exception as e:
            logger.error(f"Error rejecting friend request from {friend_id}: {e}", exc_info=True)
            self.db.rollback()
            raise

    def cancel_sent_request(self, friend_id: UUID) -> dict:
        """Отменить отправленный запрос в дружбу (pending_sent)."""
        try:
            pending_request = (
                self.db.query(Friends)
                .filter(
                    Friends.user1_id == self.user_id,
                    Friends.user2_id == friend_id,
                    Friends.status == STATUS_PENDING_SENT,
                )
                .first()
            )

            if not pending_request:
                raise PendingRequestError(str(friend_id))

            self.db.delete(pending_request)
            self.db.commit()

            logger.info(f"Sent friend request to {friend_id} cancelled by {self.user_id}")

            return {"message": f"Запрос в дружбе отменён для пользователя {friend_id}", "status": "cancelled"}
        except (PendingRequestError, AcceptFriendError):
            raise
        except Exception as e:
            logger.error(f"Error cancelling sent request to {friend_id}: {e}", exc_info=True)
            self.db.rollback()
            raise

    def delete_friend(self, friend_id: UUID) -> dict:
        """Удалить друга."""
        try:
            friendship = (
                self.db.query(Friends)
                .filter(
                    Friends.user1_id == friend_id,
                    Friends.user2_id == self.user_id,
                    Friends.status == STATUS_ACCEPT,
                )
                .first()
            )

            if not friendship:
                reverse = (
                    self.db.query(Friends)
                    .filter(
                        Friends.user1_id == self.user_id,
                        Friends.user2_id == friend_id,
                        Friends.status == STATUS_ACCEPT,
                    )
                    .first()
                )
                if not reverse:
                    raise FriendNotFoundError(str(friend_id))
                friendship = reverse

            self.db.delete(friendship)
            self.db.commit()

            logger.info(f"Friend {friend_id} removed by {self.user_id}")

            return {"message": f"Друг {friend_id} удален", "status": "deleted"}
        except (FriendNotFoundError, AcceptFriendError):
            raise
        except Exception as e:
            logger.error(f"Error deleting friend {friend_id}: {e}", exc_info=True)
            self.db.rollback()
            raise
