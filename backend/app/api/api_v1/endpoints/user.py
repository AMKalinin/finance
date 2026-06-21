from uuid import UUID
from fastapi import APIRouter, Depends, Body

from app.api import deps
from app.service.user_service import User_service

router = APIRouter()

@router.get("/info")
def get_user_info(user_service: User_service = Depends(deps.get_user_service)):
    return user_service.get_user_info()

@router.get("/friends")
def get_friends(user_service: User_service = Depends(deps.get_user_service)):
    return user_service.get_friends()

@router.get("/friend-requests")
def get_friend_requests(user_service: User_service = Depends(deps.get_user_service)):
    return user_service.get_friend_requests()

@router.get("/friend-requests/sent")
def get_sent_requests(user_service: User_service = Depends(deps.get_user_service)):
    return user_service.get_sent_requests()

@router.post("/friend")
def add_friend(
    friend_id: UUID = Body(..., embed=True),
    user_service: User_service = Depends(deps.get_user_service),
):
    return user_service.add_friend(friend_id)

@router.put("/friend/accept")
def accept_friend(
    friend_id: UUID = Body(..., embed=True),
    user_service: User_service = Depends(deps.get_user_service),
):
    return user_service.accept_friend(friend_id)

@router.put("/friend/reject")
def reject_friend(
    friend_id: UUID = Body(..., embed=True),
    user_service: User_service = Depends(deps.get_user_service),
):
    return user_service.reject_friend(friend_id)

@router.put("/friend/cancel-sent")
def cancel_sent_request(
    friend_id: UUID = Body(..., embed=True),
    user_service: User_service = Depends(deps.get_user_service),
):
    return user_service.cancel_sent_request(friend_id)

@router.delete("/friend")
def delete_friend(
    friend_id: UUID = Body(..., embed=True),
    user_service: User_service = Depends(deps.get_user_service),
):
    return user_service.delete_friend(friend_id)
