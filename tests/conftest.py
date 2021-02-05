import asyncio
import logging

import pytest
from playwright.async_api import Page

from facebook_rss.browser.browser import Browser

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
@pytest.mark.asyncio
async def page():
    browser = Browser()
    await browser.start()
    page: Page = await browser.new_page()
    logger.info("New page created")
    yield page
    await browser.shutdown()
