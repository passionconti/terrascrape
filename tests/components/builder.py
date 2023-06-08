from terrascrape.builder.models.job import Job
from terrascrape.core.builder import Builder


class SampleBuilder(Builder):
    class Contents(Builder.Contents):
        source_id: int = ...
        source_type: str = ...

    def create_jobs(self, contents: Contents):
        return [
            Job(
                name='test_job01',
                tasks=['task_01', 'task_02']
            ),
            Job(
                name='test_job02',
                tasks=['task_03', 'task_04']
            )
        ]

    @property
    def topic(self):
        return 'sample_builder'
