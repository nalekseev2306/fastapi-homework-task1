from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    ORIGINS: str
    PORT: int
    ROOT_PATH: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    AUTH_ALGORITHM: str
    SECRET_AUTH_KEY: str

    SQLITE_URL: str

    @property
    def origins_list(self) -> List[str]:
        if not self.ORIGINS:
            return ["*"]
        return [origin.strip() for origin in self.ORIGINS.split(",")]

    class Config:
        env_file = '../.env'
        env_file_encoding = "utf-8"


settings = Settings()
