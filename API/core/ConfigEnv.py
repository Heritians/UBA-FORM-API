"""Config class for handling env variables.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ALGORITHM: str
    DATABASE_URI: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    ADMIN_ID: str
    ADMIN_PWD: str
    ADMIN_VILLAGE_NAME: str
    ADMIN_ROLE: str
    USER_ROLE: str
    OWNER_ROLE: str


    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
