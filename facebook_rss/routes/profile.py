from typing import List

from fastapi import APIRouter, Response, Depends
from playwright.async_api import Page

from facebook_rss.browser.browser import get_browser
from facebook_rss.browser.mbasic.profile import ProfilePage
from facebook_rss.config import Settings, get_settings
from facebook_rss.db.session import get_db
from facebook_rss.models.post import Post
from facebook_rss.routes import CommonQueryParams
from facebook_rss.rss.rss_generator import RSSGenerator
from facebook_rss.utils.decorators import cached, requires_login

profile_router = r = APIRouter()


@r.get("/profile/{profile}")
@requires_login
@cached
async def get_profile(profile: str, commons: CommonQueryParams = Depends(),
                      browser=Depends(get_browser), db=Depends(get_db),
                      settings: Settings = Depends(get_settings)):
    page: Page = await browser.new_page()
    profile_page = await ProfilePage.create(page, profile)
    posts: List[Post] = await profile_page.get_posts(full=commons.full, limit=commons.limit)
    rss_generator = RSSGenerator(posts, profile)
    rss_feed = rss_generator.generate_feed()
    await page.close()
    return Response(content=rss_feed, media_type="application/xml")
