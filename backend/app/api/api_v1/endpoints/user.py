from uuid import UUID
from fastapi import APIRouter, Depends

from app.api import deps
from app.service.user_service import User_service 

router = APIRouter()


@router.get("/info")
def get_user_info(user_service: User_service = Depends(deps.get_user_service)):
    return user_service.get_user_info()

@router.get("/friends")
def get_friends(user_service: User_service = Depends(deps.get_user_service)):
    return user_service.get_friends()

@router.post("/friend")
def add_friend(friend_id:UUID, user_service: User_service = Depends(deps.get_user_service)):
    return user_service.add_friend(friend_id)

@router.put("/friend/accept")
def accept_friend(friend_id:UUID, user_service: User_service = Depends(deps.get_user_service)):
    return user_service.accept_friend(friend_id)

@router.put("/friend/reject")
def reject_friend(friend_id:UUID, user_service: User_service = Depends(deps.get_user_service)):
    return user_service.reject_friend(friend_id)

@router.delete("/friend")
def delete_friend(friend_id:UUID, user_service: User_service = Depends(deps.get_user_service)):
    return user_service.delete_friend(friend_id)

