import os

from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("TOKEN")
BASE_URL = "http://localhost:8001/api/v1"
