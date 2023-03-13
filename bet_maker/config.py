import pydantic


class Settings(pydantic.BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    class Config:
        env_file = ".env"


settings = Settings()