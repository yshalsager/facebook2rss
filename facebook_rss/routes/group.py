from typing import List

from fastapi import APIRouter, Response, Depends
from playwright.async_api import Page

from facebook_rss.browser.browser import get_browser
from facebook_rss.browser.pages import pages
from facebook_rss.config import Settings, get_settings
from facebook_rss.db.session import get_db
from facebook_rss.models.post import Post
from facebook_rss.routes import CommonQueryParams, unauthorized, unavailable
from facebook_rss.rss.rss_generator import RSSGenerator
from facebook_rss.utils.decorators import cached

group_router = r = APIRouter()


@r.get("/group/{fb_page}")
@cached
async def get_group(fb_page: str, commons: CommonQueryParams = Depends(),
                    browser=Depends(get_browser), db=Depends(get_db),
                    settings: Settings = Depends(get_settings)):
    page: Page = await browser.new_page()
    group_page = await pages[settings.SITE]["group"].create(page, fb_page)
    is_private = await group_page.is_private
    if not settings.USE_ACCOUNT and is_private:
        await page.close()
        raise unauthorized
    if await group_page.is_not_available:
        await page.close()
        raise unavailable
    posts: List[Post] = await group_page.get_posts(
        full=commons.full, limit=commons.limit, as_text=commons.as_text, include_comments=commons.comments)
    rss_feed = RSSGenerator(posts, fb_page).generate_feed()
    await page.close()
    return Response(content=rss_feed, media_type="application/xml")
