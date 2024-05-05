from sqlalchemy import Engine
from sqlmodel import create_engine, Session
from contextlib import contextmanager

from uudex_server.core.settings import get_settings
from typing import Optional

# host = "localhost"
# database = "uudex"
# user = "uudex_user"
# password = "uudex"
# port = 5432

__engine__: Optional[Engine] = None
#engine: Engine = None #  create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}", echo=True)

def get_db_session() -> Session:
    """Retrieve a new database session each time called

    The _`ref:uudex_server.core.settings:get_settings` must have
    been called with a path before this function can be called.

    :return: A sqlalchemy `Session` object.
    :rtype: Session
    """
    global __engine__

    if __engine__ is None:
        settings = get_settings()
        __engine__ = create_engine(settings.db_uri, echo=True)

    return Session(__engine__)

# @contextmanager
# def create_session() -> Session:
#     yield Session(engine)

if __name__ == '__main__':
    from sqlmodel import select
    from uudex_server.models import Participant
    #from uudex_server.app.model import Participant

    settings = get_settings(".env-develop")
    session = get_db_session()
    statement = select(Participant)
    results = session.exec(statement)
    for rdr in results:
        print(rdr)

    # with create_session() as session:
    #     statement = select(Participant)
    #     results = session.exec(statement)
    #     for rdr in results:
    #         print(rdr)
