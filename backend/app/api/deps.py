from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID

from app.db.session import SessionLocal
from app.service.fin_app import Fin_app


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
    server_url="http://192.168.0.24:8080/",
    client_id="fin-client",
    realm_name="fin_realm",
    client_secret_key="wztpnAcy9vOCx59iqXSTQmngqiEDO4uH",
)


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://192.168.0.24:8080/realms/fin_realm/protocol/openid-connect/auth",
    tokenUrl="http://192.168.0.24:8080/realms/fin_realm/protocol/openid-connect/token",
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
