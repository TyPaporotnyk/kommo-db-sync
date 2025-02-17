from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL, pool_pre_ping=True, echo=False, echo_pool=False
)

session_maker = sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=False, autocommit=False
)


@contextmanager
def get_session():
    session = session_maker()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
