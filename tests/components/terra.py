import requests

from terrascrape.core.terra import Terra


class RealAPITESTTerra(Terra):
    @property
    def name(self):
        return 'real_api_test_terra'

    class Parameters(Terra.Parameters):
        user_id: int = ...

    def fetch(self, parameters: Parameters):
        return requests.get(f'https://jsonplaceholder.typicode.com/todos/{str(parameters.user_id)}',
                            verify=False).json()

    def validate(self, fetched_data):
        return fetched_data.get('userId') is not None
