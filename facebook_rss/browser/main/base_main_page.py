# pylint: disable=R0801
from abc import ABC

from playwright.async_api import Page

from facebook_rss.browser.common.fb_page import BaseFBPage


class BaseMainPage(BaseFBPage, ABC):

    def __init__(self, page: Page):
        super().__init__(page)
        self._is_main_page = True

    @property
    def _comment_author_selector(self):
        return "//div[contains(@aria-label, 'Comment')]/div[2]//a/span/span"

    @property
    def _comment_content_selector(self):
        return "//div[contains(@aria-label, 'Comment')]//div[contains(text(), ' ')]"

    @property
    def _comments_selector(self):
        return "//div[contains(@aria-label, 'Comment')]"

    @property
    def _not_available_selector(self):
        return "//span[contains(text(), 'Right Now')]"
