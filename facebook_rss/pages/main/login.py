# pylint: disable=R0801
from playwright.async_api import Page

from facebook_rss.pages.common.login import BaseLoginPage


class LoginPage(BaseLoginPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._url = "https://www.facebook.com/login/"

    @classmethod
    async def create(cls, page: Page):
        self = LoginPage(page)
        current_url = await self.get_actual_url()
        if current_url != self.url:
            await self.open(self.url)
        return self

    @property
    def email(self):
        return "#email"

    @property
    def password(self):
        return "#pass"

    @property
    def login_btn(self):
        return "#loginbutton"
