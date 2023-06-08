from terrascrape.db import Base
from terrascrape.db import Column, JSON
from terrascrape.db.models.component import ComponentMixin


class Builder(ComponentMixin, Base):
    __tablename__ = 'builders'

    contents_schema = Column(JSON, nullable=True)
