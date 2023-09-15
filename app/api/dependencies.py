from typing import Generator

from app.api.session import TimescaleSessionProvider
from settings import settings

time_scale_session_provider = TimescaleSessionProvider(settings=settings)


def get_analytics_db() -> Generator:
    try:
        db = time_scale_session_provider.session()
        yield db
    finally:
        db.close()
