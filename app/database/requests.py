from sqlalchemy import select, create_engine, update
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


def get_user(tg_id):
    with Session(engine) as session:
        user = session.scalar(select(User).where(
            User.tg_id == tg_id  # noqa
        ))
        return user


def get_all_major():
    with Session(engine) as session:
        return session.scalars(select(Major)).fetchall()


def add_user_information(tg_id, user_data):
    with Session(engine) as session:
        # noinspection PyTypeChecker
        stmt = (
            update(User).where(tg_id == User.tg_id).values(
                first_name=user_data['first_name'],
                second_name=user_data['second_name'],
                position=user_data['position'],
                degree=user_data['degree'],
                course=user_data['course'],
                major_id=user_data['major'],
                number=user_data['number'],
                is_questioned=True
            )
        )
        session.execute(stmt)
        session.commit()
