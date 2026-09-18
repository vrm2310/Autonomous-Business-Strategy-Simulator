from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

from abss.db.session import SessionLocal


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()