from terrascrape.db.models.task import Task


def test_add_task(test_db_session):
    test_db_session.add(
        Task(
            name='test_add_task',
            package_name='tests.db.models.test_task',
            class_name='TestAddTask',
            required_criteria_keys=['id', 'date'],
            required_tasks=['test_sub_task']
        )
    )
    task = test_db_session.query(Task).filter(Task.name == 'test_add_task').one()
    assert 'id' in task.required_criteria_keys
    assert 'test_sub_task' in task.required_tasks
