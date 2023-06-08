from terrascrape.db import BigInteger, Column, DateTime, String, TEXT, declared_attr, func


class ComponentMixin(object):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    package_name = Column(String(200), nullable=False)
    class_name = Column(String(200), nullable=False)
    description = Column(TEXT, nullable=True)

    @declared_attr
    def created_at(cls):
        return Column(DateTime, nullable=False, default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
