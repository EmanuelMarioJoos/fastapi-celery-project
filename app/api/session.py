import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TimescaleSessionProvider:
    def __init__(self, settings):
        self.engine = create_engine(
            _create_timescale_url(settings),
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=80,
        )
        self.session = self._create_session_maker()

    def _create_session_maker(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


def _create_timescale_url(settings):
    password = settings.TIMESCALE_PASSWORD
    username = settings.TIMESCALE_USERNAME
    host = settings.TIMESCALE_HOST_URL
    port = settings.TIMESCALE_PORT
    dbname = settings.TIMESCALE_DATABASE_NAME
    return f"postgresql://{username}:{password}@{host}:{port}/{dbname}"