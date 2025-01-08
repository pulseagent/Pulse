from pydantic import Field
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    API_KEYS: list[str] = Field(default_factory=list)
