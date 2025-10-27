from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL:str = "postgresql+psycopg2://postgres:123@localhost:5432/managerJWT"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()