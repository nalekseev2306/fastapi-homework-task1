from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    ORIGINS: str = ''
    PORT: int = 8000
    ROOT_PATH: str = '/api/v1'

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    AUTH_ALGORITHM: str = 'HS256'
    SECRET_AUTH_KEY: str = 'aF75A92Cd9s10KGL4nLdt1r85XRtZ7APNO6NheGeKdRBhhc9oObQywxmqPF'

    SQLITE_URL: str = 'sqlite:///../data/test.db'

    @property
    def origins_list(self) -> List[str]:
        if not self.ORIGINS:
            return ["*"]
        return [origin.strip() for origin in self.ORIGINS.split(",")]

    class Config:
        env_file = '.env'
        env_file_encoding = "utf-8"


settings = Settings()
