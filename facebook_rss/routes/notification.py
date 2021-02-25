from typing import List

from fastapi import APIRouter, Response, Depends
from playwright.async_api import Page

from facebook_rss.browser.browser import get_browser
from facebook_rss.browser.pages import pages
from facebook_rss.config import Settings, get_settings
from facebook_rss.db.session import get_db
from facebook_rss.models.notification import Notification
from facebook_rss.routes import minimal_parameters
from facebook_rss.rss.rss_generator import NotificationRSSGenerator
from facebook_rss.utils.decorators import cached, requires_login, requires_auth

notifications_router = r = APIRouter()


@r.get("/notifications/", tags=["notifications"])
@requires_auth
@requires_login
@cached
async def get_notifications(fb_page: str = "notifications", browser=Depends(get_browser),
                            commons: dict = Depends(minimal_parameters), db=Depends(get_db),
                            settings: Settings = Depends(get_settings)):
    """
    Get feeds of your account notifications.
    """
    site = commons["site"] or settings.SITE
    page: Page = await browser.new_page()
    notifications_page = await pages[site]["notification"].create(page)
    notifications: List[Notification] = await notifications_page.get_notifications()
    rss_feed = NotificationRSSGenerator(notifications).generate_feed()
    await browser.get_cookies()
    await page.close()
    return Response(content=rss_feed, media_type="application/xml")
