from abc import ABC, abstractmethod
from inspect import getfile
from os import environ, path
from typing import Optional


class Component(ABC):
    @property
    def package_name(self) -> str:
        root = environ.get('PYTHONPATH').split(':')[0]
        directory, file = path.split(getfile(self.__class__))
        dirname = path.relpath(directory, root)
        filename = path.splitext(file)[0]
        return '.'.join([*dirname.split('/'), filename])

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError(f'implement {self.class_name} name')

    @property
    def description(self) -> Optional[str]:
        return None
