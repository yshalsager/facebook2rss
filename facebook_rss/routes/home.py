from fastapi import APIRouter
from playwright.async_api import Page

from facebook_rss import browser

router = APIRouter()


@router.get("/home/")
async def get_home_feed():
    page: Page = await browser.new_page()
    await page.goto("http://mbasic.facebook.com/")
    title = await page.title()
    await page.close()
    return {"title": title}
