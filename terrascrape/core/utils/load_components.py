import abc
import inspect
import pathlib
import sys
import types
import typing

from terrascrape.core.component import Component

MODULE_PREFIX = '__get_classes_for__'


def is_class_imported(file: pathlib.Path, class_name: str) -> bool:
    return f'import {class_name}\n' in get_code_string_in_file(file)


def is_inherited_class(child_class: object, parent_class: object) -> bool:
    return parent_class in get_all_bases_in_class(child_class)


def get_all_bases_in_class(class_obj: object, previous_bases: typing.List[object] = None) -> typing.List[object]:
    previous_bases = previous_bases or []
    bases = [base for base in class_obj.__bases__ if base not in [abc.ABC, object, *previous_bases]]
    for base in bases:
        bases.extend(get_all_bases_in_class(base, bases))
    return bases


def get_classes_in_file(file: pathlib.Path) -> typing.Dict[str, object]:
    module_key = f'{MODULE_PREFIX}{file.stem}'
    module = types.ModuleType(module_key)
    module.__file__ = str(file.absolute())
    sys.modules[module_key] = module
    exec(get_code_string_in_file(file), module.__dict__)
    classes = inspect.getmembers(sys.modules[module_key], inspect.isclass)
    return {class_name: class_obj for class_name, class_obj in classes}


def get_code_string_in_file(file: pathlib.Path) -> str:
    with open(file.absolute(), 'r') as f:
        code = f.read()
    return code


def get_files_imported_class_in_directory(directory: str, class_name: str) -> typing.List[pathlib.Path]:
    files = []
    for file in list(pathlib.Path(directory).rglob('*.py')):
        if is_class_imported(file, class_name):
            files.append(file)
    return files


def get_inheritance_classes_in_directory(directory: str, class_obj: object) -> typing.List[object]:
    inheritance_classes = []
    for file in get_files_imported_class_in_directory(directory, class_obj.__name__):
        for name, cls in get_classes_in_file(file).items():
            if is_inherited_class(cls, class_obj):
                inheritance_classes.append(cls)
    return inheritance_classes


def load_components(directory: str, component: typing.Type[Component]) -> typing.List[Component]:
    components = {}
    for class_obj in get_inheritance_classes_in_directory(directory, component):
        class_instance = class_obj()
        if class_instance.name in components:
            raise Exception(f'{class_instance.class_name}: {class_instance.name} is already registered')
        else:
            components[class_instance.name] = class_instance
    return list(components.values())


def reset_modules_to_get_classes_in_file():
    for module in list(sys.modules.keys()):
        if MODULE_PREFIX in module:
            del sys.modules[module]
