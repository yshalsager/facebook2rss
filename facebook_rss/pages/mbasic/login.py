# pylint: disable=R0801
from playwright.async_api import Page

from facebook_rss.pages.common.login import BaseLoginPage


class LoginPage(BaseLoginPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._url = "https://mbasic.facebook.com/login/"
        self._not_now_btn = '//a[contains(@href, "regular_login")]'

    @classmethod
    async def create(cls, page: Page):
        self = LoginPage(page)
        current_url = await self.get_actual_url()
        if current_url != self.url:
            await self.open(self.url)
        return self

    @property
    def email(self):
        return '//input[@name="email"]'

    @property
    def password(self):
        return '//input[@name="pass"]'

    @property
    def login_btn(self):
        return '//input[@name="login"]'

    async def skip_save(self):
        if "save-device" in await self.get_actual_url():
            async with self.page.expect_navigation():
                await self.page.click(self._not_now_btn)
