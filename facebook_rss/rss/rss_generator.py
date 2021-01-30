from html import escape
from typing import List

from feedgen.feed import FeedGenerator

from facebook_rss.models.post import Post
from facebook_rss.utils.html import clean_urls


class RSSGenerator:
    feed: FeedGenerator
    posts: List[Post]

    def __init__(self, posts, fb):
        self.fb = fb
        self.posts = posts
        self.feed = FeedGenerator()

    def generate_feed(self):
        name = self.posts[0].author
        self.feed.title(name)
        self.feed.link(href=f"https://www.facebook.com/{self.fb}/posts?_fb_noscript=1", rel="alternate")
        self.feed.description(name)
        self.feed.logo(self.posts[0].logo)
        for post in self.posts:
            entry = self.feed.add_entry()
            entry.title(post.title)
            entry.link(href=post.url, rel='alternate')
            entry.description(escape(clean_urls(post.html)))
        return self.feed.rss_str().decode('utf-8')
