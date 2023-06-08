from terrascrape.db.models import ScrapStatus
from terrascrape.db.models.message_status import MessageStatus


def test_add_message_status(test_db_session):
    test_db_session.add(MessageStatus(
        message_uuid='test',
        topic='test',
        message={'key': 'value'},
        worker_thread_id='thread1',
    ))
    message = test_db_session.query(MessageStatus).filter(MessageStatus.message_uuid == 'test').one()
    assert message.status == ScrapStatus.READY
    assert message.retry_count == 0
    assert message.finished_jobs == []
