from sqlalchemy import inspect


def test_db_engine_meta(test_db_engine, test_db_table):
    assert 'test_models' in inspect(test_db_engine).get_table_names()


def test_db_session_execute_query(test_db_session):
    assert 'test_models' in [
        row.tablename for row in test_db_session.execute('''
            SELECT tablename
            FROM pg_catalog.pg_tables WHERE schemaname = 'public'
        ''').fetchall()
    ]
