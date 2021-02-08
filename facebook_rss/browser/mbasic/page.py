from playwright.async_api import Page

from facebook_rss.browser.mbasic.profile import ProfilePage


class FBPage(ProfilePage):

    def __init__(self, page: Page, page_id: str):
        super().__init__(page, page_id)

    @classmethod
    async def create(cls, page: Page, profile: str):
        self = FBPage(page, profile)
        current_url = await self.get_actual_url()
        if current_url != self.url:
            await self.open(self.url)
        return self
