from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.orm import Session


class UnitOfWork:
    def __init__(self, session: Session) -> None:
        self.session = session

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def close(self) -> None:
        self.session.close()

    @contextmanager
    def transaction(self) -> Generator[Session, None, None]:
        try:
            yield self.session
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise