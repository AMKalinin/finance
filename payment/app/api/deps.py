from fastapi import HTTPException, status
from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID, KeycloakAdmin


from keycloak import KeycloakOpenIDConnection

keycloak_connection = KeycloakOpenIDConnection(
                        server_url="http://192.168.0.24:8080/",
                        username="test123",
                        password="123",
                        realm_name="fin_realm",
                        client_id="admin-cli")

keycloak_admin = KeycloakAdmin(connection=keycloak_connection)


# keycloak_admin = KeycloakAdmin(
#     server_url="http://192.168.0.24:8080/",
#     username='admin',
#     password='1234',
#     realm_name="master",
#     user_realm_name="fin_realm",
#     verify=True)
# keycloak_admin.realm_name = "fin_realm"


keycloak_openid = KeycloakOpenID(
    server_url="http://192.168.0.24:8080/",
    client_id="payment-client",
    realm_name="fin_realm",
    client_secret_key="sznaOFLiP2eoVMuMjcRqOJlO2vTEJots",
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://192.168.0.24:8080/realms/fin_realm/protocol/openid-connect/auth",
    tokenUrl="http://192.168.0.24:8080/realms/fin_realm/protocol/openid-connect/token",
    scopes={"openid": "openID"},
)

def check_token(token: str):
    err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token_info = keycloak_openid.introspect(token) 
        if not token_info['active']:
            print("Токен недействителен или отозван")
            raise err
        else:
            print("Токен действителен") 
    except Exception as e:
        print(f"Ошибка при проверке токена: {e}")
        raise err

def get_current_user(token: str = Depends(oauth2_scheme)):
    check_token(token)
    print(keycloak_admin.users_count())
    try:
        userinfo = keycloak_openid.userinfo(token)
        return userinfo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

