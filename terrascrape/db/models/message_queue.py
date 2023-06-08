import enum

from terrascrape.db import Base
from terrascrape.db import BigInteger, Column, DateTime, Enum, Index, String, func


class MessagePriority(enum.Enum):
    HIGHEST = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    LOWEST = 5


class MessageQueue(Base):
    __tablename__ = 'message_queue'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    message_uuid = Column(String(200), nullable=False, unique=True)
    topic = Column(String(200), nullable=False)
    priority = Column(Enum(MessagePriority), nullable=False, default=MessagePriority.NORMAL)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('index_message_queue_on_topic_priority', topic, priority),
    )
