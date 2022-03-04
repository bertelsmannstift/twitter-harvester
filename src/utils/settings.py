# import dependencies
from pydantic import BaseSettings


class Settings(BaseSettings):

    TWITTER_BEARERTOKEN: str
    TWITTER_APIKEY: str
    TWITTER_APIKEYSECRET: str

    class Config:
        env_file = ".env"

settings = Settings()
