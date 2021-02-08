__version__ = '0.3.0'

from pathlib import Path
from typing import Optional

path: Path = Path(__package__).absolute()
config_path: Path = path.parent
cookies_file_name: str = "session"
local_cookies: Optional[Path] = Path(config_path / cookies_file_name) if Path(
    config_path / cookies_file_name).exists() else None
