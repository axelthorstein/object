import os


def get_env():
    return os.environ.get("ENV", "development")


def set_config():
    env = get_env()

    if env == "development":
        os.environ["URL"] = "https://localhost:8080"
    elif env == "production":
        os.environ["URL"] = "https://object-is.appspot.com"

    return env


ENV = set_config()
