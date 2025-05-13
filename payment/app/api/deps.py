from fastapi import HTTPException, status
from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID

keycloak_openid = KeycloakOpenID(
    server_url="http://192.168.0.24:8080/",
    client_id="payment_client",
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

def get_fin_service(token: str = Depends(oauth2_scheme)):
    return get_current_user(token)
