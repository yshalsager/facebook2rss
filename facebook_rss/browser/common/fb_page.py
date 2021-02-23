# pylint: disable=R0801
import json
import re
from abc import abstractmethod, ABC
from datetime import datetime
from typing import List

from nested_lookup import nested_lookup
from playwright.async_api import Page, ElementHandle

from facebook_rss.browser.common.base_page import BasePage
from facebook_rss.models.post import Post
from facebook_rss.utils.html import strip_tags, clean_urls
from facebook_rss.utils.misc import random_sleep


class BaseFBPage(BasePage, ABC):

    def __init__(self, page: Page):
        super().__init__(page)
        self._is_group = False
        self._is_main_page = False

    @property
    @abstractmethod
    def posts_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _author_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _attached_link_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _image_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _post_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _post_content_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _post_text_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _publish_date_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _video_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _comment_author_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _comment_content_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _comments_selector(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _not_available_selector(self):
        raise NotImplementedError

    @property
    async def is_not_available(self):
        return bool(await self.page.query_selector(self._not_available_selector))

    async def get_posts(self, full: int = 0, limit: int = 0, as_text: int = 0, include_comments: int = 0) -> List[Post]:
        posts = []
        posts_urls = []
        if self._is_main_page:
            script = [await i.inner_html() for i in await self.page.query_selector_all('script') if
                      'share_fbid' in await i.inner_html()][0]
            posts = [i for i in nested_lookup('story', json.loads(
                re.search(r'{\"define.*\);}\);}\);', script).group().replace(');});});', ''))) if
                     (i.get('url') or i.get('permalink')) and ('/posts/' in i.get('url') or 'permalink' in i.get('url'))
                     and i.get('creation_time')]
            posts_urls: List[str] = sorted([i['url'] for i in posts], key=lambda x: x.split('/')[:-1],
                                           reverse=not self._is_group)
        if not self._is_group:
            start = 0
        else:
            if posts_urls:
                start = 1 if len(posts_urls) > 1 else 0
            else:
                start = 1
        if not full:
            if not self._is_group:
                posts_count = 1
            else:
                if posts_urls:
                    posts_count = len(posts_urls)
                else:
                    posts_count = 2
        else:
            posts_count: int = len(await self.page.query_selector_all(self.posts_selector))
        posts_items = []
        for item in range(start, posts_count):
            if limit and item > limit:
                continue
            full_text = ""
            post_html = None
            if not self._is_main_page:
                posts: List[ElementHandle] = await self.page.query_selector_all(self.posts_selector)
            if posts_urls:
                post_url = posts_urls[item]
            else:
                post_url = await posts[item].get_attribute('href')
                if post_url.startswith('/'):
                    post_url = f"https://mbasic.facebook.com{post_url}"
                else:
                    post_url = post_url.replace("m.facebook", "mbasic.facebook")
            await self.open(post_url)
            await self.page.wait_for_selector(self._post_selector)
            post = await self.page.query_selector(self._post_selector)
            if not posts_urls:
                date = await post.query_selector(self._publish_date_selector)
                if date:
                    date = await date.text_content()
            else:
                date = datetime.fromtimestamp(posts[item]['creation_time'])
            profile_name = await post.query_selector(self._author_selector)
            if profile_name:
                profile_name = await profile_name.text_content()
                full_text = f"{profile_name} posted:\n"
            if not as_text:
                post_html = ""
                html_parts = await self.page.query_selector_all(
                    f"{self._post_selector}{self._post_content_selector}") \
                    if not posts_urls else await self.page.query_selector(
                    f"{self._post_selector}{self._post_content_selector}")
                if isinstance(html_parts, list):
                    for part in html_parts:
                        post_html += strip_tags(await part.inner_html())
                else:
                    post_html += strip_tags(await html_parts.inner_html())
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
                # TODO: Fix wrong comments in main site
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
