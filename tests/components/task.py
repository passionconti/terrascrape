from terrascrape.core.task import Task


class PrepareOneTask(Task):
    @property
    def name(self):
        return 'prepare_1'

    def run(self):
        return


class PrepareTwoTask(Task):
    @property
    def name(self):
        return 'prepare_2'

    def run(self):
        return


class ProcessOneTask(Task):
    @property
    def name(self):
        return 'process_1'

    @property
    def required_criteria_keys_in_job(self):
        return ['aaa', 'bbb']

    def run(self):
        return


class ProcessTwoTask(Task):
    @property
    def name(self):
        return 'process_2'

    @property
    def required_criteria_keys_in_job(self):
        return ['aaa', 'bbb']

    @property
    def required_tasks_in_job(self):
        return ['process_1']

    def run(self):
        return


class FinalOneTask(Task):
    @property
    def name(self):
        return 'final_1'

    @property
    def required_criteria_keys_in_job(self):
        return ['aaa', 'bbb']

    def run(self):
        return


class SetConfigTask(Task):
    @property
    def name(self):
        return 'set_config'

    def run(self):
        self.set_config('key', 'value')


class GetConfigTask(Task):
    @property
    def name(self):
        return 'get_config'

    @property
    def required_tasks_in_job(self):
        return ['set_config']

    def run(self):
        value_from_config = self.get_from_config('key')
        return f'{value_from_config} comes from config'


class LoadResultTask(Task):
    @property
    def name(self):
        return 'load_result'

    @property
    def required_tasks_in_job(self):
        return ['get_config']

    def run(self):
        return self.load_from_job_results('get_config') + ' loaded'
