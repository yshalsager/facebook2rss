from typing import List

from fastapi import APIRouter, Response
from playwright.async_api import Page

from facebook_rss import browser
from facebook_rss.models.post import Post
from facebook_rss.pages.mbasic.profile import ProfilePage
from facebook_rss.rss.rss_generator import RSSGenerator

router = APIRouter()


@router.get("/profile/{profile}")
async def get_profile(profile: str):
    page: Page = await browser.new_page()
    profile_page = await ProfilePage.create(page, profile)
    posts: List[Post] = await profile_page.get_posts()
    rss_generator = RSSGenerator(posts, profile)
    await page.close()
    return Response(content=rss_generator.generate_feed(), media_type="application/xml")
