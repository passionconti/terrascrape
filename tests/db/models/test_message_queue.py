from terrascrape.db.models.message_queue import MessagePriority, MessageQueue


def test_add_normal_priority_scrap_message_queue(test_db_session):
    test_db_session.add(MessageQueue(message_uuid='test', topic='test'))
    message = test_db_session.query(MessageQueue).filter(MessageQueue.topic == 'test').one()
    test_db_session.query(MessageQueue).filter(MessageQueue.topic == 'test').delete()
    assert message.priority == MessagePriority.NORMAL
