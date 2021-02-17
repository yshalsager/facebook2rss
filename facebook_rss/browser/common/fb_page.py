import re
from abc import abstractmethod, ABC
from typing import List

from playwright.async_api import Page, ElementHandle

from facebook_rss.browser.common.base_page import BasePage
from facebook_rss.models.post import Post
# pylint: disable=R0801
from facebook_rss.utils.html import strip_tags, clean_urls
from facebook_rss.utils.misc import random_sleep


class BaseFBPage(BasePage, ABC):

    def __init__(self, page: Page):
        super().__init__(page)
        self._author_selector = None
        self._attached_link_selector = None
        self._comment_author_selector = 'h3'
        self._comment_content_selector = 'div[1]'
        self._comments_selector = '//div[contains(@id, "actions")]/following-sibling::div/div/div'
        self._image_selector = None
        self._post_selector = None
        self._post_content_selector = None
        self._post_text_selector = None
        self._publish_date_selector = None
        self._video_selector = None
        self._url = ""
        self._is_group = False
        self._not_available_selector = "//span[contains(text(), 'cannot be displayed right now') or" \
                                       " contains(text(), 'was not found')]"

    @property
    @abstractmethod
    def posts_selector(self):
        raise NotImplementedError

    @property
    async def is_not_available(self):
        return bool(await self.page.query_selector(self._not_available_selector))

    async def get_posts(self, full: int = 0, limit: int = 0, as_text: int = 0, include_comments: int = 0) -> List[Post]:
        start = 1 if self._is_group else 0
        if not full:
            posts_count = 2 if self._is_group else 1
        else:
            posts_count: int = len(await self.page.query_selector_all(self.posts_selector))
        posts_items = []
        for item in range(start, posts_count):
            if limit and item > limit:
                continue
            full_text = ""
            post_html = None
            posts: List[ElementHandle] = await self.page.query_selector_all(self.posts_selector)
            post_url = await posts[item].get_attribute('href')
            if post_url.startswith('/'):
                post_url = f"https://mbasic.facebook.com{post_url}"
            else:
                post_url = post_url.replace("m.facebook", "mbasic.facebook")
            await self.open(post_url)
            post = await self.page.query_selector(self._post_selector)
            date = await post.query_selector(self._publish_date_selector)
            if date:
                date = await date.text_content()
            profile_name = await post.query_selector(self._author_selector)
            if profile_name:
                profile_name = await profile_name.text_content()
                full_text = f"{profile_name} posted:\n"
            if not as_text:
                post_html = ""
                html_parts = await self.page.query_selector_all(f"{self._post_selector}{self._post_content_selector}")
                for part in html_parts:
                    post_html += strip_tags(await part.inner_html())
                post_html = re.sub(r'href=\"/', 'href=\"https://facebook.com/', post_html, re.M)
                text_obj = await post.query_selector(self._post_text_selector)
                text = await text_obj.text_content()
                title = f"{text[:30]}..."
            else:
                if date:
                    full_text += date
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
            if include_comments:
                comments = await self.page.query_selector_all(self._comments_selector)
                if comments:
                    for comment in comments:
                        comment_content = await comment.query_selector(f"xpath={self._comment_content_selector}")
                        comment_author = await comment.query_selector(f"xpath={self._comment_author_selector}")
                        comment_author_text = await comment_author.text_content()
                        if not as_text:
                            comment_html = strip_tags(await comment_content.inner_html())
                            comment_html = re.sub(r'href=\"/', 'href=\"https://facebook.com/', comment_html, re.M)
                            post_html += f'<br><br>{comment_author_text}: {comment_html}'
                        else:
                            comment_text = await comment.text_content()
                            full_text += f'\n\n{comment_author_text}: {comment_text}'
            if full:
                await random_sleep()
            posts_items.append(
                Post(url=clean_urls(await self.get_actual_url()),
                     title=title,
                     content=full_text if as_text else clean_urls(post_html),
                     author=profile_name,
                     date=date)
            )
            await self.back()
        return posts_items
