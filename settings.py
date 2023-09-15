from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    CELERY_BROKER_URL: str = Field(default='redis://127.0.0.1:6379/0', env='CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND: str = Field(default='redis://127.0.0.1:6379/0', env='CELERY_RESULT_BACKEND')
    REDIS_URL: str = Field(default='redis://127.0.0.1:6379/0', env='REDIS_URL')

    CELERY_BEAT_SCHEDULE: dict = {
        "do_periodic_stuff": {
            "task": "dummy_periodic_task",
            "schedule": 10,
            'options': {'queue': 'periodic'},
        },
    }
    CELERY_TIMEZONE: str = "Europe/Zurich"

    TIMESCALE_PASSWORD: str = Field(default='password', env="TIMESCALE_PASSWORD")
    TIMESCALE_USERNAME: str = Field(
        default="postgres", env="TIMESCALE_USERNAME"
    )
    TIMESCALE_HOST_URL: str = Field(default='127.0.0.1', env="TIMESCALE_HOST_URL")
    TIMESCALE_PORT: str = Field(default=27992, env="TIMESCALE_PORT")
    TIMESCALE_DATABASE_NAME: str = Field(default='postgres', env="TIMESCALE_DATABASE_NAME")


class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"
    case_sensitive = True


settings = Settings()
