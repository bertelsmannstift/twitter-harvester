# import dependencies
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):

    TWITTER_BEARERTOKEN: str
    TWITTER_APIKEY: str
    TWITTER_APIKEYSECRET: str

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    @property
    def sql_connection(self) -> str:
        """str: Synchronous Application connection string."""
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"


@ lru_cache()
def get_settings():
    return Settings()
