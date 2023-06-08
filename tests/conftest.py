import os
import tempfile

from pytest import fixture

from terrascrape.configuration import load_configuration
from terrascrape.core.utils.update_components import update_whole_components
from terrascrape.db import Base, Column, DateTime, Integer, String, TEXT, func
from terrascrape.db import engine, session
from terrascrape.db.models.message_status import MessageStatus
from terrascrape.db.services import DBService


class TestModel(Base):
    __tablename__ = 'test_models'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    note = Column(TEXT, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())


@fixture(scope='session')
def test_config_file_path():
    with tempfile.TemporaryDirectory() as test_config_dir:
        test_config_loc = os.path.join(test_config_dir, "test_config.toml")
        with open(test_config_loc, "wb") as test_default_config:
            test_default_config.write(b"""
            subscribe_count = 1

            [server]
            host = "http://localhost"
            port = "4242"
            host_port = "4242"
            host_ip = "127.0.0.1"
            endpoint = "${server.host}:${server.port}"

            [server.database]
            drivername = "postgresql"
            host = "db"
            port = "5432"
            database = "terrascrape"
            username = "terrascrape"
            password = "password"
            """)
        yield test_config_loc


@fixture(scope='session')
def test_config(test_config_file_path):
    yield load_configuration(test_config_file_path)


@fixture(scope='session')
def test_db_engine(test_config):
    return engine(test_config)


@fixture(scope='session')
def test_db_table(test_db_engine):
    Base.metadata.create_all(bind=test_db_engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=test_db_engine)


@fixture(scope='session')
def test_db_session(test_db_engine, test_db_table):
    connection = test_db_engine.connect()
    transaction = connection.begin()
    db_session = session(test_db_engine)

    yield db_session

    db_session.close()
    transaction.rollback()
    connection.close()


@fixture(scope='session')
def test_message_uuid_from_db(test_db_session):
    DBService(test_db_session)
    update_whole_components(os.path.join(os.path.dirname(__file__), 'components'))
    message_status = MessageStatus(
        message_uuid='test_message',
        topic='test_message_topic',
        message={
            'uuid': 'test_message',
            'topic': 'test_message_topic',
            'contents': {
                'business_id': 1,
            },
            'jobs': [
                {
                    'name': 'prepare_job',
                    'tasks': ['prepare_1', 'prepare_2'],
                    'trigger': 'ANY',
                },
                {
                    'name': 'process_job',
                    'tasks': ['process_1', 'process_2'],
                    'criteria': {'aaa': 1, 'bbb': 2},
                    'trigger': 'SUCCEED',
                },
                {
                    'name': 'final_job',
                    'tasks': ['final_1'],
                    'criteria': {'aaa': 1, 'bbb': 2},
                    'trigger': 'FAILED',
                },
            ]
        },
        worker_thread_id='thread1',
    )
    test_db_session.add(message_status)
    return message_status.message_uuid


@fixture(scope='session')
def test_message_for_task_uuid_from_db(test_db_session):
    DBService(test_db_session)
    update_whole_components(os.path.join(os.path.dirname(__file__), 'components'))
    message_status = MessageStatus(
        message_uuid='test_message_for_task',
        topic='test_message_for_task_topic',
        message={
            'uuid': 'test_message_for_task',
            'topic': 'test_message_for_task_topic',
            'contents': {
                'business_id': 1,
            },
            'jobs': [
                {
                    'name': 'job_for_task',
                    'tasks': [
                        'set_config',
                        'get_config',
                        'load_result',
                    ],
                    'trigger': 'ANY',
                },
            ]
        },
        worker_thread_id='thread1',
    )
    test_db_session.add(message_status)
    return message_status.message_uuid


@fixture(scope='session')
def test_message_to_check_required_task_uuid_from_db(test_db_session):
    DBService(test_db_session)
    update_whole_components(os.path.join(os.path.dirname(__file__), 'components'))
    message_status = MessageStatus(
        message_uuid='test_message_to_check_required_task',
        topic='test_message_to_check_required_topic',
        message={
            'uuid': 'test_message_to_check_required_task',
            'topic': 'test_message_to_check_required_topic',
            'contents': {
                'business_id': 1,
            },
            'jobs': [
                {
                    'name': 'job_to_check_required_task',
                    'tasks': [
                        'get_config',
                        'load_result',
                    ],
                    'trigger': 'ANY',
                },
            ]
        },
        worker_thread_id='thread1',
    )
    test_db_session.add(message_status)
    return message_status.message_uuid
