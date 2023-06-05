import pydantic


class Settings(pydantic.BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_PORT: int
    TEST_POSTGRES_DB: str

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_EXCHANGE: str
    RABBITMQ_EVENTS_QUEUE: str

    class Config:
        env_file = ".env"


settings = Settings()