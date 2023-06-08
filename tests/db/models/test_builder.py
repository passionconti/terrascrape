from terrascrape.db.models.builder import Builder


def test_add_builder(test_db_session):
    test_db_session.add(
        Builder(
            name='test_db_builder',
            package_name='tests.db.models.test_builder',
            class_name='TestBuilder'
        )
    )
    builder = test_db_session.query(Builder).filter(Builder.name == 'test_db_builder').one()
    assert builder.name == 'test_db_builder'
    assert builder.class_name == 'TestBuilder'
