from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID

from app.core.config import settings
from app.db.session import SessionLocal
from app.service.fin_app import Fin_app
from app.service.user_service import User_service

def get_db():
    try:
        db = SessionLocal()
        yield db
    # except:
    #     db.rollback()
    # else:
    #     db.commit()
    finally:
        db.close()
    #return SessionLocal()


keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_URL,
    client_id=settings.KEYCLOAK_CLIENT_NAME,
    realm_name=settings.KEYCLOAK_REALM_NAME,
    client_secret_key=settings.KEYCLOAK_SECRET_FINSLI_API,
    verify=False
)


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.AUTHORIZATION_URL,
    tokenUrl=settings.TOKEN_URL,
    scopes={"openid": "openID"},
)


def get_current_user(token: str):
    try:
        userinfo = keycloak_openid.userinfo(token)
        return userinfo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_fin_service(token: str = Depends(oauth2_scheme)) -> Generator[Fin_app, ..., ...]:
     try:
        user = get_current_user(token)
        db = next(get_db())
        f_app = Fin_app(db, user)
        yield f_app
     finally:
        db.close()

def get_user_service(token:str = Depends(oauth2_scheme)) -> Generator[User_service, ..., ...]:
    try:
        user = get_current_user(token)
        db = next(get_db())
        user_service = User_service(db, user)
        yield user_service
    finally:
        db.close()
