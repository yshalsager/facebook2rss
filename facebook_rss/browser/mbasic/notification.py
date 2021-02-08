from typing import List

from playwright.async_api import Page

from facebook_rss.browser.common.fb_page import BaseFBPage
# pylint: disable=R0801
from facebook_rss.models.notification import Notification
from facebook_rss.models.post import Post


class NotificationPage(BaseFBPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._url = "https://mbasic.facebook.com/notifications.php"
        self._notifications_selector = '//a[contains(@href, "/notifications.php?") and not(@accesskey)]'
        self._notification_text_selector = 'div/span'
        self._notification_date_selector = '//span/abbr'

    @classmethod
    async def create(cls, page: Page):
        self = NotificationPage(page)
        current_url = await self.get_actual_url()
        if current_url != self.url:
            await self.open(self.url)
        return self

    async def get_posts(self, full: int = 0, limit: int = 0, as_text: int = 0, include_comments: int = 0) -> List[Post]:
        raise NotImplementedError

    @property
    def posts_selector(self):
        return ''

    async def get_notifications(self) -> List[Notification]:
        notifications_item = []
        notifications = await self.page.query_selector_all(self._notifications_selector)
        if notifications:
            for notification in notifications[:-1]:
                url = await notification.get_attribute('href')
                notification_content = await notification.query_selector(f"xpath={self._notification_text_selector}")
                notification_content = await notification_content.text_content()
                notification_date = await notification.query_selector(self._notification_date_selector)
                notification_date = await notification_date.text_content()
                notifications_item.append(
                    Notification(url=f"https://mbasic.facebook.com{url}",
                                 content=notification_content,
                                 date=notification_date)
                )
        return notifications_item
