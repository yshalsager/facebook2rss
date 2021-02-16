from abc import ABC

from playwright.async_api import Page

from facebook_rss.browser.common.base_page import BasePage


# pylint: disable=R0801


class BaseLoginCheckpointPage(BasePage, ABC):

    def __init__(self, page: Page):
        super().__init__(page)
        self._url = ""
        self._code_form_selector = ""
        self._continue_selector = ""

    async def login(self):
        code = input("Enter your 2FA code: ")
        form = await self.page.query_selector(self._code_form_selector)
        await form.tap()
        await self.page.fill(self._code_form_selector, code)
        async with self.page.expect_navigation():
            await self.page.keyboard.press("Enter")
        await self.page.click(self._continue_selector)
