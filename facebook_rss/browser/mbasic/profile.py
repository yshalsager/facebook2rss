from playwright.async_api import Page

from facebook_rss.browser.common.fb_page import BaseFBPage


# pylint: disable=R0801

class ProfilePage(BaseFBPage):

    def __init__(self, page: Page, profile: str):
        super().__init__(page)
        self._url = f"https://mbasic.facebook.com/{profile}?v=timeline"
        self._post_selector = "//div[contains(@data-ft,'top_level_post_id')]"
        self._author_selector = "//strong/a[last()]"
        self._publish_date_selector = "abbr"
        self._post_text_selector = "//p"
        self._attached_link_selector = "a.bo.bp"
        self._image_selector = "img"
        self._video_selector = "//a[starts-with(@href, '/video_redirect/')]"

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
