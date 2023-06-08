from terrascrape.db.models.message_status import MessageStatus
from terrascrape.db.services import DBService


class MessageStatusService(DBService):
    def __init__(self):
        self._session = DBService()._session

    def get(self, message_uuid: str):
        return self._session.query(MessageStatus).filter(MessageStatus.message_uuid == message_uuid).first()
