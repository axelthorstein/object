import os
import json
from multiprocessing import Lock

OBJECT_DIR = os.getcwd()
LOCK = Lock()


class ConfigException(Exception):
    pass


class Environments:
    development = 'development'
    circleci = 'circleci'
    production = 'production'


def current_environment():
    """Return the name of the current executing environment.

    Returns:
        str: The current environemnt.
    """
    if os.environ.get('CIRCLECI') == 'true':
        return Environments.circleci
    return os.environ.get('PYTHON_ENV', Environments.development)


def relative_config_file_path(file_name):
    """Return the config file path based on the environment.

    Args:
        file_name (str): The file name to be loaded.

    Returns:
        str: The config file path.
    """
    return f"/configs/{file_name}"


def absolute_config_file_path(relative_config_path):
    """Return the config path relative to the OS.

    Args:
        relative_config_path (str): The config file path.

    Returns:
        str: The relative config file path.
    """
    return os.path.normpath(OBJECT_DIR + relative_config_path)


def get_config(config_file):
    """Return the config file.

    Args:
        config_file (str): The config file path.

    Returns:
        dict: The config file contents.

    Raises:
        ConfigException: If there is an issue loading the config file.
    """
    with open(config_file) as f:
        try:
            config = json.load(f)
        except ValueError:
            raise ConfigException(
                f"The {config_file} file could not be loaded.")

    return config


def load_config(file_name):
    """Return the config based on the environment.

    Returns:
        dict: The config file contents.
    """
    relative_config = relative_config_file_path(file_name)
    config_file = absolute_config_file_path(relative_config)
    config = get_config(config_file)

    return config


SEQUENCES = load_config('product_map.json')
