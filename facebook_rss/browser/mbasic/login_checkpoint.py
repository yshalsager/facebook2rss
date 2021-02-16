from playwright.async_api import Page

# pylint: disable=R0801
from facebook_rss.browser.common.login_checkpoint import BaseLoginCheckpointPage


class LoginCheckpointPage(BaseLoginCheckpointPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._url = "https://mbasic.facebook.com/checkpoint/"
        self._code_form_selector = "#approvals_code"
        self._continue_selector = "#checkpointSubmitButton-actual-button"

    @classmethod
    async def create(cls, page: Page):
        self = LoginCheckpointPage(page)
        current_url = await self.get_actual_url()
        if current_url != self.url:
            await self.open(self.url)
        return self
