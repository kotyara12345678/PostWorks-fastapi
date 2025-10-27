import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "PostWorks FastAPI"
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://mongo:27017")  # если mongo в контейнере называется "mongo"
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "postworks_db")
    USERS_SERVICE_URL: str = os.getenv(
        "USERS_SERVICE_URL", "http://fastapiproject2-web-1:8000"
    )
settings = Settings()