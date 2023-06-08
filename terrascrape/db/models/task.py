from terrascrape.db import ARRAY, Column, String
from terrascrape.db import Base
from terrascrape.db.models.component import ComponentMixin


class Task(ComponentMixin, Base):
    __tablename__ = 'tasks'

    required_criteria_keys = Column(ARRAY(String(200)), nullable=True)
    required_tasks = Column(ARRAY(String(200)), nullable=True)
