from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID, KeycloakError

from app.core.config import settings
from app.db.session import SessionLocal
from app.service.fin_app import Fin_app
from app.service.user_service import User_service 
from app.err.errors import AuthenticationError, DatabaseError
from app.logging_config import get_logger

logger = get_logger(__name__)

def get_db() -> Generator[SessionLocal, None, None]:
    """
    Получение базы данных.
    Создает новую сессию для каждого запроса и закрывает её в конце.
    """
    db = SessionLocal()
    try:
        yield db
        # db.commit()
    except Exception as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise DatabaseError(f"Ошибка базы данных: {str(e)}")
    finally:
        db.close()


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
    """
    Получение информации о пользователе из Keycloak.
    
    Args:
        token: Bearer токен аутентификации
        
    Returns:
        dict: Информация о пользователе (user_id, email и др.)
        
    Raises:
        AuthenticationError: Если токен невалиден или истек
    """
    try:
        userinfo = keycloak_openid.userinfo(token)
        logger.info(f"User authenticated: {userinfo.get('sub')}")
        return userinfo
    except KeycloakError as e:
        logger.warning(f"Keycloak authentication failed: {e}")
        raise AuthenticationError("Ошибка аутентификации через Keycloak")
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {e}")
        raise AuthenticationError("Неверные учетные данные")

def get_fin_service(token: str = Depends(oauth2_scheme)) -> Generator[Fin_app, ..., None]:
    """
    Получение сервиса Fin_app с авторизацией.
    
    Yields:
        Fin_app: Сервис для работы с финансами
    """
    try:
        user = get_current_user(token)
        db = next(get_db())
        f_app = Fin_app(db, user)
        yield f_app
    except AuthenticationError:
        raise
    except Exception as e:
        logger.error(f"Error in get_fin_service: {e}")
        raise DatabaseError("Ошибка при инициализации сервиса")

def get_user_service(token: str = Depends(oauth2_scheme)) -> Generator[User_service, ..., None]:
    """
    Получение сервиса User_service с авторизацией.
    
    Yields:
        User_service: Сервис для работы с пользователем
    """
    try:
        user = get_current_user(token)
        db = next(get_db())
        user_service = User_service(db, user)
        yield user_service
    except AuthenticationError:
        raise
    except Exception as e:
        logger.error(f"Error in get_user_service: {e}")
        raise DatabaseError("Ошибка при инициализации сервиса пользователя")
