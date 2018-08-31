import os
import json
from pathlib import Path
from multiprocessing import Lock

OBJECT_DIR = os.getcwd()
LOCK = Lock()


class ConfigException(Exception):
    pass


class Environments:
    development = 'development'
    circleci = 'circleci'
    production = 'production'


def save_credentials_file(file_path):
    """Save the application default credentials service account to a file.

    Args:
        file_path: The path to the credentials file.

    Returns:
        str: Path to the saved credentials file.
    """
    if not Path(file_path).exists():
        with open(file_path, 'w') as f:
            json.dump(
                json.loads(os.environ['APPLICATION_DEFAULT_CREDENTIALS']), f)

    return file_path


def generate_color_range_map():
    """Return a hash map of hue value to color name for fast access.

    Create this map a single time at the beginning of execution to reduce
    runtime.

    Todo:
        Make sure this only gets called on app startup.

    Returns:
        Dict[int, str]: The hue to color name hash map.
    """
    color_range_map = {}
    color_ranges_map = {
        range(0, 7): 'red',
        range(7, 45): 'orange',
        range(45, 80): 'yellow',
        range(80, 180): 'green',
        range(180, 260): 'blue',
        range(260, 300): 'purple',
        range(300, 360): 'red'
    }

    for color_range in color_ranges_map:
        for value in color_range:
            color_range_map[value] = color_ranges_map[color_range]

    return color_range_map


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


PRODUCT_MAP = load_config('product_map.json')

COLOR_CODE_MAP = load_config('color_code_map.json')

COLOR_RANGE_MAP = generate_color_range_map()

CREDENTIALS_FILE = save_credentials_file('configs/cloud_credentials.ejson')
