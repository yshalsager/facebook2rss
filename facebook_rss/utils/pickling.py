from pathlib import Path
from pickle import load, dump, HIGHEST_PROTOCOL

from facebook_rss import config_path, cookies_file_name


def pickle_(cookies: list):
    with open(config_path / cookies_file_name, "wb") as cookies_file:
        dump(cookies, cookies_file, protocol=HIGHEST_PROTOCOL)


def unpickle(file: Path) -> list:
    if file and file.exists():
        with open(file, 'rb') as cookies_file:
            return load(cookies_file)
