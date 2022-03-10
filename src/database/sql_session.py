"""SQL sessions."""

from contextlib import contextmanager
from typing import Iterator

from models.base import Base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from database.sql import engine

# Queries are sent to the respective database depending from which base they were derived from
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=True,
    expire_on_commit=False,
    binds={Base: engine},
)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Start context manager for a complete session lifecycle.

    Example:
        with session_scope() as session:
            do_stuff()

    Yields
    ------
    Session
        SQLAlchemy Session object.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    Base.metadata.create_all(bind=engine)
