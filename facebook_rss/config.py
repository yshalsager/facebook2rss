from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Facebook to RSS API"
    LOG_DIR: str = f"{str(Path(__file__).absolute().parent)}/logs/"
    # Playwright Browser Connection
    PROXY_SERVER: str = ""  # Supports http and socks proxies.
    PROXY_USERNAME: str = ""
    PROXY_PASSWORD: str = ""
    # Facebook related settings
    LANGUAGE_CODE: str = "en"  # Supports EN only currently.
    SITE: str = "mbasic"
    USE_ACCOUNT: bool = True
    # RSS settings
    EXPIRATION_TIME: int = 30  # Time in minutes for cached feeds to expire after


@lru_cache()
def get_settings():
    return Settings()
