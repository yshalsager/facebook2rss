from typing import List

from fastapi import APIRouter, Response, Depends, HTTPException
from playwright.async_api import Page

from facebook_rss.browser.browser import get_browser
from facebook_rss.browser.mbasic.profile import ProfilePage
from facebook_rss.config import Settings, get_settings
from facebook_rss.db.session import get_db
from facebook_rss.models.post import Post
from facebook_rss.rss.rss_generator import RSSGenerator
from facebook_rss.utils.decorators import cached

profile_router = r = APIRouter()


@r.get("/profile/{profile}")
@cached
async def get_profile(profile: str, browser=Depends(get_browser), db=Depends(get_db),
                      settings: Settings = Depends(get_settings)):
    if not settings.USE_ACCOUNT:
        raise HTTPException(
            status_code=403,
            detail="You cannot access Facebook profiles without enabling USE_ACCOUNT option and logged in.")
    page: Page = await browser.new_page()
    profile_page = await ProfilePage.create(page, profile)
    posts: List[Post] = await profile_page.get_posts()
    rss_generator = RSSGenerator(posts, profile)
    rss_feed = rss_generator.generate_feed()
    await page.close()
    return Response(content=rss_feed, media_type="application/xml")
