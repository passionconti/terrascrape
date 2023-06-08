from abc import abstractmethod

from terrascrape.core.component import Component
from terrascrape.db.services import DBService
from terrascrape.exceptions import SERVICE_ERROR_ALREADY_REGISTERED, ServiceException


class ComponentService(DBService):
    def __init__(self, db_component):
        self._session = DBService()._session
        self._db_component = db_component
        self.__load_names()

    def __load_names(self, name: str = None):
        if name:
            self._names.append(name)
        else:
            self._names = [component.name for component in self.get_all()]

    @abstractmethod
    def _map_component_to_db_model(self, component: Component):
        raise NotImplementedError('implement _map_component_to_db_model')

    def insert(self, component: Component):
        if component.name in self._names:
            raise ServiceException(SERVICE_ERROR_ALREADY_REGISTERED.format(component.name),
                                   extra=dict(location=f'{self.__class__.__name__}.insert'))
        self._session.add(self._map_component_to_db_model(component))
        self.__load_names(component.name)

    def get(self, name: str):
        return self._session.query(self._db_component).filter(self._db_component.name == name).first()

    def get_all(self):
        return self._session.query(self._db_component).all()

    def reset(self):
        self._session.query(self._db_component).delete()
        self.__load_names()
