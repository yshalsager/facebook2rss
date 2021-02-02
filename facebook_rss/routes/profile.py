from typing import List

from fastapi import APIRouter, Response, Depends
from playwright.async_api import Page

from facebook_rss import browser
from facebook_rss.db.session import get_db
from facebook_rss.models.post import Post
from facebook_rss.pages.mbasic.profile import ProfilePage
from facebook_rss.rss.rss_generator import RSSGenerator
from facebook_rss.utils.cached import cached

profile_router = r = APIRouter()


@r.get("/profile/{profile}")
@cached
@browser.refresh_cookies
async def get_profile(profile: str, db=Depends(get_db)):
    page: Page = await browser.new_page()
    profile_page = await ProfilePage.create(page, profile)
    posts: List[Post] = await profile_page.get_posts()
    rss_generator = RSSGenerator(posts, profile)
    rss_feed = rss_generator.generate_feed()
    await page.close()
    return Response(content=rss_feed, media_type="application/xml")
