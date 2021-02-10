__version__ = '0.4.0'

import logging.config
from pathlib import Path
from typing import Optional

import yaml

path: Path = Path(__package__).absolute()
config_path: Path = path.parent
cookies_file_name: str = "session"
local_cookies: Optional[Path] = Path(config_path / cookies_file_name) if Path(
    config_path / cookies_file_name).exists() else None

logging.config.dictConfig(yaml.load(Path(path / 'logging_conf.yml').read_text(), Loader=yaml.FullLoader))
