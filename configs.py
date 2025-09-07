from pydantic_settings import BaseSettings, SettingsConfigDict


class BasicSettings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", enable_decoding="utf8", strict=False)

    MODE: str
    VERSION: str


basic_settings = BasicSettings()
