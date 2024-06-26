
from typing import List, Union

from sendgrid import SendGridAPIClient
from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    SENDGRID_API_KEY: str

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str,
                              List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    async def SENDGRID_CLIENT(cls) -> SendGridAPIClient:
        return SendGridAPIClient(cls.SENDGRID_API_KEY)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
