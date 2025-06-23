from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class BcryptSettings:
    default_rounds_value: int = 12


class DB_Config(BaseModel):
    db_name: str
    db_user: str
    db_password: str
    db_port: int
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@localhost:{self.db_port}/{self.db_name}"


class Auth(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


class ApiPrefix(BaseModel):
    user: str = "/user"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    db_config: DB_Config
    auth: Auth
    api: ApiPrefix = ApiPrefix()


settings = Config()
