from sqlalchemy.orm.session import Session

from terrascrape.configuration import config
from terrascrape.db import engine, session
from terrascrape.utils.singleton import Singleton


class DBService(metaclass=Singleton):
    def __init__(self, db_session: Session = None):
        self._session = db_session or session(engine(config))
