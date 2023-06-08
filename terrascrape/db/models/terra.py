from terrascrape.db import Base
from terrascrape.db import Boolean, Column, JSON
from terrascrape.db.models.component import ComponentMixin


class Terra(ComponentMixin, Base):
    __tablename__ = 'terras'

    parameters_schema = Column(JSON, nullable=False)
    is_valid = Column(Boolean, default=True, nullable=False)
