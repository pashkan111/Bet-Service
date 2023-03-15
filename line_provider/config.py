import pydantic


class Settings(pydantic.BaseSettings):
    BET_MAKER_CALLBACKS_URL: str
    BET_MAKER_CHANGE_EVENT_STATUS_ENDPOINT: str

    class Config:
        env_file = ".env"


settings = Settings()