import pytest
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session

from abss.db.unit_of_work import UnitOfWork


def test_transaction_commits(db_session: Session) -> None:
    unit_of_work = UnitOfWork(db_session)

    with unit_of_work.transaction() as session:
        session.execute(
            text(
                "CREATE TEMP TABLE transaction_test "
                "(id INTEGER)"
            )
        )
        session.execute(
            text(
                "INSERT INTO transaction_test (id) "
                "VALUES (1)"
            )
        )

    result = db_session.scalar(
        text("SELECT COUNT(*) FROM transaction_test")
    )

    assert result == 1


def test_transaction_rolls_back_on_exception(
    db_session: Session,
) -> None:
    unit_of_work = UnitOfWork(db_session)

    with pytest.raises(RuntimeError), unit_of_work.transaction() as session:
        session.execute(
            text(
                "CREATE TEMP TABLE rollback_test "
                "(id INTEGER)"
            )
        )
        session.execute(
            text(
                "INSERT INTO rollback_test (id) "
                "VALUES (1)"
            )
        )
        raise RuntimeError("simulate failure")

    # The temporary table creation and insert were rolled back.
    with pytest.raises(ProgrammingError):
        db_session.execute(
            text("SELECT COUNT(*) FROM rollback_test")
        )