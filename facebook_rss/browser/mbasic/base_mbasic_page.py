# pylint: disable=R0801
from abc import ABC

from playwright.async_api import Page

from facebook_rss.browser.common.fb_page import BaseFBPage


class BaseMBasicPage(BaseFBPage, ABC):

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def _comment_author_selector(self):
        return 'h3'

    @property
    def _comment_content_selector(self):
        return 'div[1]'

    @property
    def _comments_selector(self):
        return '//div[contains(@id, "actions")]/following-sibling::div/div/div'

    @property
    def _not_available_selector(self):
        return "//span[contains(text(), 'cannot be displayed right now') or" \
               " contains(text(), 'was not found')]"
