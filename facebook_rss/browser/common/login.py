from abc import abstractmethod, ABC

from playwright.async_api import Page

from facebook_rss.browser.common.base_page import BasePage


class BaseLoginPage(BasePage, ABC):

    def __init__(self, page: Page):
        self._url = ""
        super().__init__(page)

    @property
    def url(self):
        return self._url

    @property
    @abstractmethod
    def email(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def password(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def login_btn(self):
        raise NotImplementedError

    async def login(self, email, password):
        await self.page.fill(self.email, email)
        await self.page.fill(self.password, password)
        async with self.page.expect_navigation():
            await self.page.click(self.login_btn)
        return True
