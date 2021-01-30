from abc import abstractmethod, ABC
from typing import List

from playwright.async_api import Page

from facebook_rss.pages.common.base_page import BasePage


class BaseProfilePage(BasePage, ABC):

    def __init__(self, page: Page):
        self._url = ""
        super().__init__(page)

    @property
    def url(self):
        return self._url

    @property
    @abstractmethod
    def posts_selector(self):
        raise NotImplementedError

    @abstractmethod
    async def get_posts(self) -> List[str]:
        raise NotImplementedError
