from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    API_KEYS: list[str] = []
    TWITTER_TOKEN: str = ""


SETTINGS = Settings()
