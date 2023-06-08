from terrascrape.db import Base, Column, TEXT
from terrascrape.db.models.component import ComponentMixin


class CustomComponent(ComponentMixin, Base):
    __tablename__ = 'custom_components'

    note = Column(TEXT, nullable=True)


def test_create_component_table(test_db_session):
    assert 'custom_components' in [
        row.tablename for row in test_db_session.execute('''
            SELECT tablename
            FROM pg_catalog.pg_tables WHERE schemaname = 'public'
        ''').fetchall()
    ]


def test_add_component_model(test_db_session):
    test_db_session.add(
        CustomComponent(
            name='test_component_model',
            package_name='tests.db.models.test_component',
            class_name='TestCustomComponent',
            note='test for component custom model',
        )
    )
    task = test_db_session.query(CustomComponent).filter(CustomComponent.name == 'test_component_model').one()
    assert task is not None
