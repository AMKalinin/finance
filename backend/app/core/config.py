import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    API_V1_STR: str = "/api/v1"

    POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    POSTGRES_HOSTNAME = os.environ.get("POSTGRES_HOSTNAME")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
    SQLALCHEMY_DATABASE_URI = (
        f"{POSTGRES_SERVER}+psycopg2://{POSTGRES_USER}:"
        + f"{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:"
        + f"{POSTGRES_PORT}/{POSTGRES_DB}"
    )[0]
    SQLALCHEMY_DATABASE_URI = "sqlite:///finance_db.sqlite"

    
    KEYCLOAK_URL = os.environ.get("KC_URL")
    KEYCLOAK_SECRET_FINSLI_API = os.environ.get("KC_CLIENT_SECRET_KEY_FINSI_API")
    AUTHORIZATION_URL = f'{KEYCLOAK_URL}realms/alkal_realm/protocol/openid-connect/auth'
    TOKEN_URL = f'{KEYCLOAK_URL}realms/alkal_realm/protocol/openid-connect/token'
settings = Settings()

print(settings.AUTHORIZATION_URL)
print(settings.TOKEN_URL)
print(settings.KEYCLOAK_URL)
print(settings.POSTGRES_SERVER)
