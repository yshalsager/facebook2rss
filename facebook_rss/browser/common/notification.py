# pylint: disable=R0801
from abc import ABC, abstractmethod
from typing import List

from playwright.async_api import Page

from facebook_rss.browser.common.base_page import BasePage
from facebook_rss.models.notification import Notification


class BaseNotificationPage(BasePage, ABC):

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    @abstractmethod
    def url(self):
        return NotImplementedError

    @property
    @abstractmethod
    def _notifications_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _notification_text_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _notification_date_selector(self):
        raise NotImplementedError

    async def get_notifications(self) -> List[Notification]:
        notifications_item = []
        await self.page.wait_for_selector(self._notifications_selector)
        notifications = await self.page.query_selector_all(self._notifications_selector)
        if notifications:
            for notification in notifications[:-1]:
                url = await notification.get_attribute('href')
                notification_content = await notification.query_selector(f"xpath={self._notification_text_selector}")
                notification_content = await notification_content.text_content()
                notification_date = await notification.query_selector(self._notification_date_selector)
                notification_date = await notification_date.text_content()
                notifications_item.append(
                    Notification(url=f"https://mbasic.facebook.com{url}" if not url.startswith('http') else url,
                                 content=notification_content,
                                 date=notification_date)
                )
        return notifications_item
