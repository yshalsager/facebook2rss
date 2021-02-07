import re
from typing import List

from playwright.async_api import Page, ElementHandle

from facebook_rss.browser.common.profile import BaseProfilePage
from facebook_rss.models.post import Post
# pylint: disable=R0801
from facebook_rss.utils.html import strip_tags, get_url_without_tracking
from facebook_rss.utils.misc import random_sleep


class ProfilePage(BaseProfilePage):

    def __init__(self, page: Page, profile: str):
        super().__init__(page)
        self._url = f"https://mbasic.facebook.com/{profile}?v=timeline"
        self._post_selector = "//div[contains(@data-ft,'top_level_post_id')]"
        self._author_selector = "//strong/a"
        self._publish_date_selector = "abbr"
        self._post_text_selector = "//p"
        self._attached_link_selector = "a.bo.bp"
        self._image_selector = "img"
        self._video_selector = "//a[starts-with(@href, '/video_redirect/')]"

    @classmethod
    async def create(cls, page: Page, profile: str):
        self = ProfilePage(page, profile)
        current_url = await self.get_actual_url()
        if current_url != self.url:
            await self.open(self.url)
        return self

    @property
    def posts_selector(self):
        # return '//article[contains(@data-ft,"top_level_post_id")]//p'
        return '//a[contains(@href, "/story.php?") and contains(text(), "Full Story")]'

    async def get_posts(self, full: int = 0, limit: int = 0) -> List[Post]:
        if not full:
            posts_count = 1
        else:
            posts_count: int = len(await self.page.query_selector_all(self.posts_selector))
        posts_items = []
        for item in range(0, posts_count):
            if limit and item > limit:
                continue
            full_text = ""
            posts: List[ElementHandle] = await self.page.query_selector_all(self.posts_selector)
            post = posts[item]
            await post.click()
            post = await self.page.query_selector(self._post_selector)
            post_html = strip_tags(await post.inner_html())
            post_html = re.sub(r'href=\"/', 'href=\"https://facebook.com/', post_html, re.MULTILINE)
            profile_name = await post.query_selector(self._author_selector)
            if profile_name:
                profile_name = await profile_name.text_content()
                full_text = f"{profile_name} posted:\n"
            date = await post.query_selector(self._publish_date_selector)
            if date:
                full_text += f"{await date.text_content()}\n"
            text_chunks = await post.query_selector_all(self._post_text_selector)
            text = [await i.text_content() for i in text_chunks]
            text = '\n'.join(text) + '\n'
            title = f"{text[:30]}..."
            full_text += text
            attached_link = await post.query_selector(self._attached_link_selector)
            if attached_link:
                attached_link_href = await attached_link.get_attribute('href')
                if not attached_link_href.startswith("http"):
                    attached_link_href = "https://facebook.com" + attached_link_href
                attached_link_text = await attached_link.text_content()
                if attached_link_text:
                    attached_link_text = f"[{attached_link_text}]"
                full_text += f"{attached_link_text}({attached_link_href})\n"
            images = await post.query_selector_all(self._image_selector)
            if images:
                for image in images:
                    full_text += f"{await image.get_attribute('src')}\n"
            videos = await post.query_selector_all(self._video_selector)
            if videos:
                for video in videos:
                    video_link_href = await video.get_attribute('href')
                    if not video_link_href.startswith("http"):
                        video_link_href = "https://facebook.com" + video_link_href
                    full_text += f"{video_link_href}\n"
            # print(full_text)
            await random_sleep()
            posts_items.append(
                Post(url=get_url_without_tracking(await self.get_actual_url()),
                     html=post_html,
                     title=title,
                     content=full_text,
                     author=profile_name,
                     text=full_text)
            )
            await self.back()
        return posts_items
