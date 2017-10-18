import os

def get_env():
    return os.environ.get("ENV", "local")

def set_config():
    env = get_env()

    if env == "local":
        os.environ["URL"] = "https://localhost:8080"
    elif env == "production":
        os.environ["URL"] = "https://redheads-181023.appspot.com"

    return env

env = set_config()
