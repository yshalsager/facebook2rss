__version__ = '0.1.0'

from pathlib import Path
from typing import Optional

from facebook_rss.browser import Browser

path: Path = Path(__package__).absolute()
config_path: Path = path.parent
cookies_file_name: str = "session"
local_cookies: Optional[Path] = Path(config_path / cookies_file_name) if Path(config_path / cookies_file_name) else None
browser: Browser = Browser()
