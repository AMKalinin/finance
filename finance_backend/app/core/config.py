import os
from dotenv import load_dotenv


load_dotenv()

class Settings:

    API_V1_STR: str = "/api/v1"

    POSTGRES_SERVER = os.environ.get('POSTGRES_SERVER') 
    POSTGRES_USER = os.environ.get('POSTGRES_USER') 
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD') 
    POSTGRES_DB = os.environ.get('POSTGRES_DB') 
    POSTGRES_HOSTNAME = os.environ.get('POSTGRES_HOSTNAME')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
    SQLALCHEMY_DATABASE_URI = f'{POSTGRES_SERVER}+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}'


settings = Settings()