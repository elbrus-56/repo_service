from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    clickhouse_uri: str = "clickhouse://default:secret@localhost:9001/events"
    mongo_uri: str = "mongodb://root:secret@127.0.0.1:27018/events?authSource=admin"


settings = Settings()
