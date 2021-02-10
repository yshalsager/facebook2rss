from typing import List

from fastapi import APIRouter, Response, Depends
from playwright.async_api import Page

from facebook_rss.browser.browser import get_browser
from facebook_rss.browser.pages import pages
from facebook_rss.config import Settings, get_settings
from facebook_rss.db.session import get_db
from facebook_rss.models.post import Post
from facebook_rss.routes import unavailable, common_parameters
from facebook_rss.rss.rss_generator import RSSGenerator
from facebook_rss.utils.decorators import cached, requires_auth

page_router = r = APIRouter()


@r.get("/page/{fb_page}", tags=["pages"])
@requires_auth
@cached
async def get_page(fb_page: str, commons: dict = Depends(common_parameters),
                   browser=Depends(get_browser), db=Depends(get_db),
                   settings: Settings = Depends(get_settings)):
    """
    Get feeds of the given page username or id.
    """
    page: Page = await browser.new_page()
    _page = await pages[settings.SITE]["page"].create(page, fb_page)
    if await _page.is_not_available:
        await page.close()
        raise unavailable
    posts: List[Post] = await _page.get_posts(
        full=commons["full"], limit=commons["limit"], as_text=commons["as_text"], include_comments=commons["comments"])
    rss_feed = RSSGenerator(posts, fb_page).generate_feed()
    await page.close()
    return Response(content=rss_feed, media_type="application/xml")
