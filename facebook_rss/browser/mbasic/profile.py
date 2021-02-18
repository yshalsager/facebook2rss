# pylint: disable=R0801
from playwright.async_api import Page

from facebook_rss.browser.mbasic.base_mbasic_page import BaseMBasicPage


class ProfilePage(BaseMBasicPage):

    def __init__(self, page: Page, profile: str):
        super().__init__(page)
        self.account = profile

    @classmethod
    async def create(cls, page: Page, profile: str):
        self = ProfilePage(page, profile)
        current_url = await self.get_actual_url()
        if current_url != self.url:
            await self.open(self.url)
        return self

    @property
    def posts_selector(self):
        # return '//article[contains(@data-ft,"top_level_post_id")]//p'
        return '//a[contains(@href, "/story.php?") and contains(text(), "Full Story")]'

    @property
    def url(self) -> str:
        return f"https://mbasic.facebook.com/{self.account}?v=timeline"

    @property
    def _author_selector(self):
        return "//strong/a[last()]"

    @property
    def _attached_link_selector(self):
        return "a.bo.bp"

    @property
    def _image_selector(self):
        return "img"

    @property
    def _post_selector(self):
        return "//div[contains(@data-ft,'top_level_post_id')]"

    @property
    def _post_content_selector(self):
        return "//div[contains(@data-ft, '{')]"

    @property
    def _post_text_selector(self):
        return "//p"

    @property
    def _publish_date_selector(self):
        return "abbr"

    @property
    def _video_selector(self):
        return "//a[starts-with(@href, '/video_redirect/')]"
