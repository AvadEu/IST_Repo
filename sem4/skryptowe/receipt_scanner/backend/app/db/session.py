from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

engine = create_engine(settings.db_url, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Bazowa klasa deklaratywna dla wszystkich modeli ORM."""


def get_db() -> Generator[Session, None, None]:
    """Zależność FastAPI dostarczająca sesję bazy danych."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
