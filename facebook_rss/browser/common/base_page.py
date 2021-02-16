from abc import ABC, abstractmethod

from playwright.async_api import Page


class BasePage(ABC):

    def __init__(self, page: Page):
        self.page: Page = page
        self._url = ""

    @classmethod
    @abstractmethod
    async def create(cls, page: Page):
        raise NotImplementedError

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    async def get_actual_url(self):
        return self.page.url

    async def get_actual_title(self):
        return await self.page.title()

    async def open(self, url):
        await self.page.goto(url)
        await self.page.wait_for_selector('body')

    async def refresh_browser(self):
        await self.page.reload()

    async def back(self):
        await self.page.go_back()

    async def forward(self):
        await self.page.go_forward()

    async def implicitly_wait(self, time: int):
        """
        wait for a timeout
        :param time: timeout in seconds
        :return:
        """
        await self.page.wait_for_timeout(time * 1000)

    async def set_window_size(self, width, height):
        await self.page.set_viewport_size({"width": width, "height": height})
