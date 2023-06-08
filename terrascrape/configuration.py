import os
from ast import literal_eval
from typing import Union

from box import Box
from toml import load

DEFAULT_CONFIG = os.path.join(os.path.dirname(__file__), "config.toml")
USER_CONFIG = os.getenv("TERRASCRAPE_USER_CONFIG_PATH", "~/.terrascrape/config.toml")
ENV_VAR_PREFIX = "TERRASCRAPE"


class Config(Box):
    pass


def string_to_type(value: str) -> Union[bool, int, float, str]:
    if value.upper() == 'TRUE':
        return True
    elif value.upper() == 'FALSE':
        return False

    try:
        eval_value = literal_eval(value)
        return eval_value
    except Exception:
        pass

    return value


def load_env_to_dict(d: dict):
    result = dict()
    for keys, value in d.items():
        current_dict = result
        keys = keys.split('__')
        for key in keys[:-1]:
            current_dict = current_dict.setdefault(key, dict())
        current_dict[keys[-1]] = string_to_type(value)

    return result


def load_configuration(default_config_path: str, user_config_path: str = None) -> Config:
    config = Config(load(default_config_path))

    if user_config_path and os.path.isfile(user_config_path):
        user_config = load(user_config_path)
        config.merge_update(user_config)

    env_config = dict()
    for env_var, env_var_value in os.environ.items():
        if env_var.startswith(ENV_VAR_PREFIX + '__'):
            env_var_key = env_var[len(ENV_VAR_PREFIX + '__'):].lower()
            env_config[env_var_key] = env_var_value
    config.merge_update(load_env_to_dict(env_config))

    return config


config: Config = load_configuration(DEFAULT_CONFIG, USER_CONFIG)
