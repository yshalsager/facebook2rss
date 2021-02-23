# pylint: disable=R0801

from playwright.async_api import Page

from facebook_rss.browser.common.notification import BaseNotificationPage


class NotificationPage(BaseNotificationPage):

    def __init__(self, page: Page):
        super().__init__(page)

    @classmethod
    async def create(cls, page: Page):
        self = NotificationPage(page)
        current_url = await self.get_actual_url()
        if current_url != self.url:
            await self.open(self.url)
        return self

    @property
    def url(self) -> str:
        return "https://www.facebook.com/notifications"

    @property
    def _notifications_selector(self):
        return '//a[contains(@href, "ref=notif")]'

    @property
    def _notification_text_selector(self):
        return '//div/span/span[(strong)]'

    @property
    def _notification_date_selector(self):
        return '//div/span/span[not(strong)]'
