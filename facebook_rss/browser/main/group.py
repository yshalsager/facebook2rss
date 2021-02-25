# pylint: disable=R0801
from playwright.async_api import Page

from facebook_rss.browser.main.profile import ProfilePage


class GroupPage(ProfilePage):

    def __init__(self, page: Page, group: str):
        super().__init__(page, group)
        self.account = group
        self._is_group = True

    @classmethod
    async def create(cls, page: Page, profile: str):
        self = GroupPage(page, profile)
        current_url = await self.get_actual_url()
        if current_url != self.url:
            await self.open(self.url)
        return self

    @property
    async def is_private(self):
        return bool(await self.page.query_selector('//span[contains(text(), "Join Group")]'))

    @property
    def url(self) -> str:
        return f"https://facebook.com/groups/{self.account}?sorting_setting=CHRONOLOGICAL"

    @property
    def _post_content_selector(self):
        return '//div[contains(text(), " ")]'

    @property
    def _post_text_selector(self):
        return f'//div[@role="article"]{self._post_content_selector}'
