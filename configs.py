from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


from app.consts import REGEX


class BasicSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="APP_", enable_decoding="utf8", strict=False, extra="ignore"
    )

    MODE: str
    VERSION: str


class PgSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="PG_", enable_decoding="utf8", strict=False, extra="ignore"
    )

    HOST: str = Field(..., pattern=REGEX.host)
    PORT: int = Field(..., ge=1, le=9999)
    DBNAME: str
    USER: str
    PASSWORD: str

    POOL_MIN_SIZE: int = Field(..., ge=1, le=10)
    POOL_MAX_SIZE: int = Field(..., ge=10, le=100)

    @computed_field
    @property
    def dsn(self) -> str:
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DBNAME}"


basic_settings = BasicSettings()

pg_settings = PgSettings()
