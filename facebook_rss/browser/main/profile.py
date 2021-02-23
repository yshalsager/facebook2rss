# pylint: disable=R0801
from playwright.async_api import Page

from facebook_rss.browser.main.base_main_page import BaseMainPage


class ProfilePage(BaseMainPage):

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
        # return f'//a[contains(@href, "/{self.account}/posts/") and @role="link" and not(contains(@href, "comment"))]'
        return "//div[@aria-posinset]"

    @property
    def url(self) -> str:
        return f"https://facebook.com/{self.account}"

    @property
    def _author_selector(self):
        return "//h2//strong/span"

    @property
    def _attached_link_selector(self):
        return '//a[@rel="nofollow noopener"]'

    @property
    def _image_selector(self):
        return "img"

    @property
    def _post_selector(self):
        return '//div[@role="article"]'

    @property
    def _post_content_selector(self):
        return '//div[@data-ad-comet-preview="message"]'

    @property
    def _post_text_selector(self):
        return '//div[@data-ad-preview="message"]'

    @property
    def _publish_date_selector(self):
        return ''

    @property
    def _video_selector(self):
        return '//a[@aria-label="Enlarge"]'
