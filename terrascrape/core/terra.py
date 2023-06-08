from abc import abstractmethod
from copy import deepcopy
from traceback import format_exc
from typing import Any

from pydantic import BaseModel, ValidationError

from terrascrape.core.component import Component
from terrascrape.exceptions import (
    TERRA_FETCH_ERROR,
    TERRA_PARAMETERS_ERROR,
    TERRA_TRANSFORM_ERROR,
    TERRA_VALIDATION_ERROR,
    TerraException,
)


class TerraResults(BaseModel):
    fetched_data: Any = ...
    transformed_data: Any = ...


class Terra(Component):
    class Parameters(BaseModel):
        pass

    @property
    def parameters_model(self) -> Parameters:
        return self.Parameters

    @abstractmethod
    def fetch(self, parameters: Parameters) -> Any:
        raise NotImplementedError('implement terra fetch logic')

    def transform(self, data) -> Any:
        return data

    def validate(self, data) -> bool:
        return True

    def run(self, **kwargs) -> TerraResults:
        try:
            parameters = self.parameters_model(**kwargs)
        except ValidationError as e:
            raise TerraException(TERRA_PARAMETERS_ERROR,
                                 extra=dict(name=self.name, exception=e.__class__, message=str(e), tb=format_exc()))

        try:
            fetched_data = self.fetch(parameters)
        except Exception as e:
            raise TerraException(TERRA_FETCH_ERROR,
                                 extra=dict(name=self.name, exception=e.__class__, message=str(e), tb=format_exc()))

        if not self.validate(deepcopy(fetched_data)):
            raise TerraException(TERRA_VALIDATION_ERROR, extra=dict(name=self.name, fetched_data=fetched_data))

        try:
            transformed_data = self.transform(deepcopy(fetched_data))
        except Exception as e:
            raise TerraException(TERRA_TRANSFORM_ERROR,
                                 extra=dict(name=self.name, exception=e.__class__, message=str(e), tb=format_exc()))

        return TerraResults(fetched_data=fetched_data, transformed_data=transformed_data)
