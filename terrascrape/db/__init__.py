from sqlalchemy import (
    ARRAY, BigInteger, Boolean, Column, Date, DateTime, Enum, ForeignKey, Index, Integer, JSON, Numeric, String, TEXT,
    func,
)
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, URL
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from terrascrape.configuration import Config, config

__all__ = [
    # sqlalchemy
    'ARRAY', 'BigInteger', 'Boolean', 'Column', 'Date', 'DateTime', 'Enum', 'ForeignKey', 'Index', 'Integer', 'JSON',
    'Numeric', 'String', 'TEXT', 'func',

    # sqlalchemy.ext.declarative
    'declarative_base', 'declared_attr',

    # sqlalchemy.orm
    'relationship',
]

Base = declarative_base()


def engine(config: Config) -> Engine:
    return create_engine(
        URL.create(
            drivername=config.server.database.drivername,
            host=config.server.database.host,
            port=config.server.database.port,
            username=config.server.database.username,
            password=config.server.database.password,
            database=config.server.database.database,
        ),
        client_encoding='utf8',
        pool_size=config.subscribe_count,
        pool_timeout=1200,
    )


def session(engine: Engine) -> Session:
    session_factory = sessionmaker(bind=engine, autocommit=config.debug)
    session = scoped_session(session_factory)
    return session()
