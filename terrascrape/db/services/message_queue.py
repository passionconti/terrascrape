from sqlalchemy import delete

from terrascrape.db.models.message_queue import MessageQueue
from terrascrape.db.services import DBService


class MessageQueueService(DBService):
    def __init__(self):
        self._session = DBService()._session

    def get(self, topic: str) -> MessageQueue:
        message = self._session.execute(
            delete(MessageQueue).where(
                MessageQueue.id.in_(
                    self._session.query(MessageQueue.id).filter(MessageQueue.topic == topic).order_by(
                        MessageQueue.priority).first() or []
                )
            ).returning(MessageQueue)
        )
        if message.rowcount == 1:
            return message.fetchone()
