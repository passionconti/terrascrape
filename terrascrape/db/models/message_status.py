from terrascrape.db import ARRAY, Column, DateTime, Enum, Index, Integer, JSON, String, TEXT, func
from terrascrape.db import Base
from terrascrape.db.models import ScrapStatus


class MessageStatus(Base):
    __tablename__ = 'message_status'

    message_uuid = Column(String(200), nullable=False, primary_key=True)
    topic = Column(String(200), nullable=False)
    message = Column(JSON, nullable=False)
    message_group_id = Column(String(200), nullable=True)
    worker_thread_id = Column(String(200), nullable=True)
    status = Column(Enum(ScrapStatus), nullable=False, default=ScrapStatus.READY)
    error_task = Column(String, nullable=True)
    error_msg = Column(TEXT, nullable=True)
    error_extra = Column(JSON(none_as_null=True), nullable=True)
    retry_count = Column(Integer, nullable=False, default=0)
    stats = Column(JSON(none_as_null=True), nullable=True)
    finished_jobs = Column(ARRAY(String), nullable=False, default=[])
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('index_message_status_on_status', 'status'),
        Index('index_message_status_on_message_group_id', 'message_group_id'),
        Index('index_message_status_on_topic_created_at', 'topic', 'created_at'),
        Index('index_message_status_on_topic_status', 'topic', 'status'),
    )
