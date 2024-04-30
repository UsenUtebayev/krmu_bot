from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from app.database.models import User, Major

engine = create_engine(url='postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')


# noinspection PyTypeChecker
def set_user(tg_id):
    with Session(engine) as session:
        user = session.scalar(select(User).where(
            User.tg_id == tg_id
        ))

        if not user:
            session.add(User(tg_id=tg_id))  # noqa
            session.commit()
            return None
        session.close()
        return user


def get_all_major():
    with Session(engine) as session:
        return session.scalars(select(Major)).fetchall()


def add_user_information(tg_id):
    with Session(engine) as session:
        user = session.scalar(select(User).where(
            User.tg_id == tg_id
        ))
