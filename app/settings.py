from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sql_alchemy_database_uri: str
    secret_key: str
    redis_uri: str


settings = Settings()