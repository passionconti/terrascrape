from pytest import fixture

from terrascrape.engine.message_handler import MessageHandler


@fixture(scope='session')
def test_message_handler(test_message_uuid_from_db):
    return MessageHandler(message_uuid=test_message_uuid_from_db)
