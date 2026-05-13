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


class User_service:
    """Сервис для работы с пользователями и друзьями."""
    
    def __init__(self, db: Session, user_info: dict):
        self.db = db
        self.user_id = UUID(user_info['sub']) if 'sub' in user_info else None
        logger.info(f"User service initialized for user {self.user_id}")
    
    def get_user_info(self) -> dict:
        """Получить информацию о пользователе."""
        try:
            user = self.db.query(User).filter(User.id == self.user_id).first()
            
            if not user:
                raise UserNotFoundError(str(self.user_id))
            
            return {
                "id": str(user.id),
                "description": user.description,
                "subscription_type": user.subscription_type,
                "subscription_expiry": user.subscription_expiry.isoformat() if user.subscription_expiry else None,
                "friends_count": len(user.friends)
            }
        except UserNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error getting user info: {e}", exc_info=True)
            raise
    
    def get_friends(self) -> List[dict]:
        """Получить список друзей."""
        try:
            friends = self.db.query(Friends).filter(
                Friends.user2_id == self.user_id
            ).all()
            
            logger.info(f"User {self.user_id} has {len(friends)} friends")
            
            return [
                {
                    "id": str(friend.user1_id),
                    "status": friend.status,
                    "created_at": friend.created_at.isoformat() if friend.created_at else None
                }
                for friend in friends
            ]
        except Exception as e:
            logger.error(f"Error getting friends: {e}", exc_info=True)
            raise
    
    def add_friend(self, friend_id: UUID) -> dict:
        """Добавить друга."""
        try:
            # Проверка существования пользователя
            friend = self.db.query(User).filter(User.id == friend_id).first()
            
            if not friend:
                raise FriendNotFoundError(str(friend_id))
            
            # Проверка на дубликат
            existing_friendship = self.db.query(Friends).filter(
                Friends.user1_id == friend_id,
                Friends.user2_id == self.user_id,
                Friends.status == "pending"
            ).first()
            
            if existing_friendship:
                raise AlreadyFriendError(str(friend_id))
            
            # Проверка взаимной дружбы
            mutual_friend = self.db.query(Friends).filter(
                Friends.user1_id == self.user_id,
                Friends.user2_id == friend_id,
                Friends.status == "accepted"
            ).first()
            
            if mutual_friend:
                raise AlreadyFriendError(str(friend_id))
            
            # Создание запроса в друзья
            new_friendship = Friends(
                user1_id=friend_id,
                user2_id=self.user_id,
                status="pending"
            )
            
            self.db.add(new_friendship)
            self.db.commit()
            
            logger.info(f"Friend request sent from {friend_id} to {self.user_id}")
            
            return {
                "id": str(new_friendship.id),
                "user1_id": str(new_friendship.user1_id),
                "user2_id": str(new_friendship.user2_id),
                "status": new_friendship.status,
                "message": f"Запрос в дружбе отправлен пользователю {friend_id}"
            }
        except (FriendNotFoundError, AlreadyFriendError):
            raise
        except Exception as e:
            logger.error(f"Error adding friend {friend_id}: {e}", exc_info=True)
            self.db.rollback()
            raise AcceptFriendError(f"Ошибка при отправке запроса в друзья: {str(e)}")
    
    def accept_friend(self, friend_id: UUID) -> dict:
        """Принять запрос в дружбу."""
        try:
            # Поиск запроса от друга к нам
            pending_request = self.db.query(Friends).filter(
                Friends.user1_id == friend_id,
                Friends.user2_id == self.user_id,
                Friends.status == "pending"
            ).first()
            
            if not pending_request:
                raise PendingRequestError(str(friend_id))
            
            # Обновление статуса
            pending_request.status = "accepted"
            self.db.commit()
            
            logger.info(f"Friend request from {friend_id} accepted by {self.user_id}")
            
            return {
                "id": str(pending_request.id),
                "user1_id": str(pending_request.user1_id),
                "user2_id": str(pending_request.user2_id),
                "status": pending_request.status,
                "message": f"Дружба подтверждена с пользователем {friend_id}"
            }
        except (PendingRequestError, AcceptFriendError):
            raise
        except Exception as e:
            logger.error(f"Error accepting friend request from {friend_id}: {e}", exc_info=True)
            self.db.rollback()
            raise
    
    def reject_friend(self, friend_id: UUID) -> dict:
        """Отклонить запрос в дружбу."""
        try:
            # Поиск запроса от друга к нам
            pending_request = self.db.query(Friends).filter(
                Friends.user1_id == friend_id,
                Friends.user2_id == self.user_id,
                Friends.status == "pending"
            ).first()
            
            if not pending_request:
                raise PendingRequestError(str(friend_id))
            
            # Удаляем запрос
            self.db.delete(pending_request)
            self.db.commit()
            
            logger.info(f"Friend request from {friend_id} rejected by {self.user_id}")
            
            return {
                "message": f"Запрос в дружбе отклонен пользователем {friend_id}",
                "status": "rejected"
            }
        except (PendingRequestError, AcceptFriendError):
            raise
        except Exception as e:
            logger.error(f"Error rejecting friend request from {friend_id}: {e}", exc_info=True)
            self.db.rollback()
            raise
    
    def delete_friend(self, friend_id: UUID) -> dict:
        """Удалить друга."""
        try:
            # Поиск дружбы (может быть в любом направлении)
            friendship = self.db.query(Friends).filter(
                Friends.user1_id == friend_id,
                Friends.user2_id == self.user_id,
                Friends.status == "accepted"
            ).first()
            
            if not friendship:
                # Проверка обратной дружбы
                reverse_friendship = self.db.query(Friends).filter(
                    Friends.user1_id == self.user_id,
                    Friends.user2_id == friend_id,
                    Friends.status == "accepted"
                ).first()
                
                if not reverse_friendship:
                    raise FriendNotFoundError(str(friend_id))
                
                friendship = reverse_friendship
            
            # Удаляем дружбу
            self.db.delete(friendship)
            self.db.commit()
            
            logger.info(f"Friend {friend_id} removed by {self.user_id}")
            
            return {
                "message": f"Друг {friend_id} удален",
                "status": "deleted"
            }
        except (FriendNotFoundError, AcceptFriendError):
            raise
        except Exception as e:
            logger.error(f"Error deleting friend {friend_id}: {e}", exc_info=True)
            self.db.rollback()
            raise
