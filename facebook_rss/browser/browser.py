import logging
from typing import Optional

from playwright.async_api import async_playwright, Browser as PBrowser, Playwright, BrowserContext

from facebook_rss import local_cookies
from facebook_rss.utils.decorators import singleton
from facebook_rss.utils.pickling import pickle_, unpickle

logger = logging.getLogger(__name__)


@singleton
class Browser:

    def __init__(self):
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[PBrowser] = None
        self._browser_context: Optional[BrowserContext] = None

    async def start(self, *args, **kwargs):
        if not self._playwright:
            self._playwright = await async_playwright().start()
            logger.info("Playwright started")
        if not self._browser:
            self._browser = await self._playwright.chromium.launch(**kwargs)
            logger.info("Browser launched")
        if not self._browser_context:
            self._browser_context = await self._browser.new_context(locale='en_US')
            logger.info("New context created")
            # if self.cookies:
            #     await self._browser_context.add_cookies(self.cookies)

    async def new_page(self):
        return await self._browser_context.new_page()

    async def add_cookies(self, cookies):
        await self._browser_context.add_cookies(cookies)

    async def shutdown(self):
        logger.info("Performing manual closing")
        await self._browser_context.close()
        await self._browser.close()
        await self._playwright.stop()

    @property
    async def cookies(self):
        return await self._browser_context.cookies()


# Dependency
async def get_browser() -> Browser:
    browser = Browser()
    await browser.start(headless=True)
    await browser.add_cookies(unpickle(local_cookies))
    try:
        yield browser
    finally:
        pickle_(await browser.cookies)
        await browser.shutdown()
