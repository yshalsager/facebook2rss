import logging

import pytest

from facebook_rss.browser.common.login import BaseLoginPage
from facebook_rss.browser.pages import pages

logger = logging.getLogger(__name__)


async def check_email(login_page: BaseLoginPage):
    email = await login_page.page.query_selector(login_page.email)
    assert email is not None


async def check_password(login_page: BaseLoginPage):
    password = await login_page.page.query_selector(login_page.password)
    assert password is not None


async def check_login_btn(login_page: BaseLoginPage):
    login_btn = await login_page.page.query_selector(login_page.login_btn)
    assert login_btn is not None


@pytest.mark.asyncio
async def test_login(page):
    logger.info("Testing login pages")
    for site, pages_dict in pages.items():
        logger.info(f"Testing {site} site login page")
        login_page_obj: BaseLoginPage = pages_dict["login"]
        login_page = await login_page_obj.create(page)
        logger.info("login page created")
        await check_email(login_page)
        await check_password(login_page)
        await check_login_btn(login_page)
