from pytest import fixture

from terrascrape.db.models.message_status import MessageStatus
from terrascrape.db.services import DBService
from terrascrape.db.services.message_status import MessageStatusService


@fixture(scope='session')
def test_message_status_service(test_db_session):
    DBService(test_db_session)
    return MessageStatusService()


def test_get_message_status_service(test_db_session, test_message_status_service):
    test_db_session.add(MessageStatus(
        message_uuid='test_get_message_status',
        topic='test-get-message-status',
        message={'key': 'value'},
        worker_thread_id='thread1',
    ))
    message = test_message_status_service.get('test_get_message_status')
    assert message.topic == 'test-get-message-status'
