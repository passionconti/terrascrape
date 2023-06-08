from terrascrape.db.models.terra import Terra


def test_add_terra(test_db_session):
    test_db_session.add(
        Terra(
            name='test_add_terra',
            package_name='tests.db.models.test_terra',
            class_name='TestAddTerra',
            parameters_schema={'title': 'Parameters', 'type': 'object',
                               'properties': {'date': {'title': 'Date', 'type': 'string'}}, 'required': ['date']},
        )
    )
    terra = test_db_session.query(Terra).filter(Terra.name == 'test_add_terra').one()
    assert terra.parameters_schema.get('title') == 'Parameters'
    assert terra.is_valid
