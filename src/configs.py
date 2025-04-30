from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str = ""
    clickhouse_uri: str = ""

settings = Settings()
