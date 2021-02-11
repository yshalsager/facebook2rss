from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from feedgen.feed import FeedGenerator
from tzlocal import get_localzone

from facebook_rss.models.notification import Notification
from facebook_rss.models.post import Post


class BaseRSSGenerator(ABC):
    feed: FeedGenerator

    def __init__(self):
        self.feed = FeedGenerator()

    @abstractmethod
    def generate_feed(self) -> str:
        raise NotImplementedError


class RSSGenerator(BaseRSSGenerator):
    posts: List[Post]

    def __init__(self, posts, fb):
        super().__init__()
        self.fb = fb
        self.posts = posts

    def generate_feed(self) -> str:
        name = self.posts[0].author
        self.feed.title(name)
        self.feed.link(href=f"https://www.facebook.com/{self.fb}/posts?_fb_noscript=1", rel="alternate")
        self.feed.description(name)
        self.feed.logo(self.posts[0].logo)
        if self.posts[0].date:
            self.feed.lastBuildDate(self.posts[0].date)
        else:
            self.feed.lastBuildDate(datetime.now(tz=get_localzone()))
        for post in self.posts:
            entry = self.feed.add_entry()
            entry.title(post.title)
            entry.link(href=post.url, rel='alternate')
            entry.guid(guid=post.url, permalink=True)
            entry.description(post.content)
            if post.date:
                entry.pubDate(post.date)
        return self.feed.rss_str().decode('utf-8')


class NotificationRSSGenerator(BaseRSSGenerator):
    notifications: List[Notification]

    def __init__(self, notifications):
        super().__init__()
        self.notifications = notifications

    def generate_feed(self) -> str:
        name = "Notifications"
        self.feed.title(name)
        self.feed.link(href="https://mbasic.facebook.com/notifications.php", rel="alternate")
        self.feed.description(name)
        self.feed.logo(self.notifications[0].logo)
        for notification in self.notifications:
            entry = self.feed.add_entry()
            entry.title(notification.title)
            entry.link(href=notification.url, rel='alternate')
            entry.description(notification.content)
            entry.pubDate(notification.date)
        return self.feed.rss_str().decode('utf-8')
