# настраиваем подключение базы данных
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Database:
    def __init__(self):
        self._db_url = "sqlite:///D:/Progi/Backend/fastapi"
        self._engine = create_engine(self._db_url)

    # аналог with для работы с сессиями
    @contextmanager
    def session(self):
        connection = self._engine.connect()

        Session = sessionmaker(bind=self._engine)
        session = Session()

        try:
            # возвращает сессию, затем вернётся
            # к выполнению функции после конца работы с ней
            yield session
            session.commit()
            session.close()
        except Exception:
            session.rollback()
            raise


database = Database()
Base = declarative_base()
