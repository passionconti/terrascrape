from pytest import fixture


@fixture(scope='session')
def test_raw_message():
    return {
        'uuid': 'test_message',
        'topic': 'test_topic',
        'contents': {
            'business_id': 1,
            'address': 'xxxxx',
        },
        'jobs': [
            {
                'name': 'prepare_job_01',
                'tasks': ['prepare_task_01', 'prepare_task_02'],
                'trigger': 'ANY',
            },
            {
                'name': 'process_job_01',
                'tasks': ['process_task_01', 'process_task_02'],
                'criteria': {'aaa': 1, 'bbb': 2},
                'trigger': 'SUCCEED',
            },
            {
                'name': 'process_job_02',
                'tasks': ['process_task_03', 'process_task_04'],
                'criteria': {'aaa': 1, 'bbb': 2},
                'on_error': 'IGNORE'
            },
            {
                'name': 'final_job_01',
                'tasks': ['final_task_01'],
                'criteria': {'aaa': 1, 'bbb': 2},
                'trigger': 'FAILED',
            },
            {
                'name': 'final_job_02',
                'tasks': ['final_task_02'],
                'trigger': 'ANY',
            }
        ]
    }
