from pytest import fixture, mark

from sqlalchemy.exc import NoResultFound

from terrascrape.db.models.message_queue import MessagePriority, MessageQueue
from terrascrape.db.services import DBService
from terrascrape.db.services.message_queue import MessageQueueService


@fixture(scope='session')
def test_message_queue_service(test_db_session):
    DBService(test_db_session)
    return MessageQueueService()


def test_get_message_queue_on_topic(test_db_session, test_message_queue_service):
    test_db_session.add(MessageQueue(message_uuid='test_get_message', topic='test-get-message'))
    message = test_message_queue_service.get('test-get-message')
    assert message.message_uuid == 'test_get_message'


def test_empty_message_queue_on_topic(test_message_queue_service):
    assert test_message_queue_service.get('test-do-not-get-message') is None


@mark.xfail(raises=NoResultFound)
def test_delete_after_get_scrap_message_queue_on_topic(test_db_session, test_message_queue_service):
    test_db_session.add(MessageQueue(message_uuid='test_delete_after_get', topic='test-delete-after-get'))
    message = test_message_queue_service.get('test-delete-after-get')
    test_db_session.query(MessageQueue).filter(MessageQueue.message_uuid == message.message_uuid).one()


def test_priority_message_queue_on_topic(test_db_session, test_message_queue_service):
    test_db_session.add_all([
        MessageQueue(message_uuid='test_priority_1', topic='test-priority'),
        MessageQueue(message_uuid='test_priority_2', topic='test-priority', priority=MessagePriority.HIGHEST)
    ])
    highest_priority_message = test_message_queue_service.get('test-priority')
    assert highest_priority_message.priority == MessagePriority.HIGHEST

    normal_priority_message = test_message_queue_service.get('test-priority')
    assert normal_priority_message.priority == MessagePriority.NORMAL
