from playwright.async_api import Page

from facebook_rss import browser
from facebook_rss.pages.common.login import BaseLoginPage
from facebook_rss.pages.pages import pages
from facebook_rss.utils.pickling import pickle_


async def login_and_get_cookies(user: str, password: str, site):
    await browser.start()
    login_page_obj: BaseLoginPage = pages[site]["login"]
    page: Page = await browser.new_page()
    login_page = await login_page_obj.create(page)
    logged_in = await login_page.login(user, password)
    if not logged_in:
        raise RuntimeError("Login failed!")
    if callable(getattr(login_page, 'skip_save', None)):
        await login_page.skip_save()
    cookies = await browser.cookies
    await page.close()
    await browser.shutdown()
    if cookies:
        pickle_(cookies)
