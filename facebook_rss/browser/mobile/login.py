# pylint: disable=R0801
from playwright.async_api import Page

from facebook_rss.browser.common.login import BaseLoginPage


class LoginPage(BaseLoginPage):

    def __init__(self, page: Page):
        super().__init__(page)

    @classmethod
    async def create(cls, page: Page):
        self = LoginPage(page)
        current_url = await self.get_actual_url()
        if current_url != self.url:
            await self.open(self.url)
        return self

    @property
    def url(self) -> str:
        return "https://m.facebook.com/login/"

    @property
    def email(self):
        return "#m_login_email"

    @property
    def password(self):
        return "#m_login_password"

    @property
    def login_btn(self):
        return '//button[@name="login"]'
