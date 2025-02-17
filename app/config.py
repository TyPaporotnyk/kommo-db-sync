from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    KOMMO_SECRET_KEY: str
    KOMMO_INTEGRATION_ID: str
    KOMMO_REDIRECT_URL: str
    KOMMO_URL_BASE: str

    @property
    def DATABASE_URL(self):
        return (
            f"mysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
