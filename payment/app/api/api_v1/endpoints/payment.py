from fastapi import APIRouter, Depends

from app.api import deps
from app.schemas.payment import payment_in
router = APIRouter()


@router.post("/create-pament")
def create_pament(*, user = Depends(deps.get_current_user), payment_info: payment_in):
    cheack_promo(user)
    send_payment(user, payment_info)
    update_subscribe_status(user, payment_info)
    return user


def cheack_promo(user):
    return True

def send_payment(user, payment_info):
    return True

def update_subscribe_status(user, payment_info):
    deps.keycloak_admin.update_user(user_id=user['sub'], payload={
        "email": user['email'],
        "attributes": {
            "isSubscribed": not user['isSubscribed'],
        }
    })
    return True
