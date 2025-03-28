from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DB_Config(BaseModel):
    db_name: str
    db_user: str
    db_password: str
    db_port: int
    
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__"
    )
    db_config: DB_Config