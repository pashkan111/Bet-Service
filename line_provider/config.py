import pydantic


class Settings(pydantic.BaseSettings):
    BET_MAKER_EXCHANGE: str
    BET_MAKER_EVENTS_ROUTING_KEY: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()