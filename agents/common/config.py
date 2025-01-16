from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ['.env', '../.env', '../../.env', '../../../.env']
        env_file_encoding = 'utf-8'
        extra = 'ignore'

    APP_NAME: str = "pulse"
    OTEL_ENABLED: bool = True
    OTEL_TRACE_UPLOAD_ENABLED: bool = False
    OTEL_TRACE_UPLOAD_URL: str = "http://127.0.0.1:4318/v1/traces"

    HOST: str = "0.0.0.0"
    PORT: int = 8080
    OPENAI_API_KEY: str = ""
    MODEL_NAME: str = "gpt-4-turbo"
    COIN_HOST: str = ""
    COIN_HOST_V2: str = ""
    COIN_API_KEY: str = ""
    COIN_API_KEY_V2: str = ""
    API_KEY: str = ""
    AI_SEARCH_HOST: str = ""
    AI_SEARCH_KEY: str = ""
    REDIS_HOST:str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = None
    REDIS_DB: int = 0
    LOG_LEVEL: str = "INFO"

SETTINGS = Settings()