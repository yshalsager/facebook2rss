from functools import wraps

from fastapi import Response

from facebook_rss.db.curd import get_feed, update_feed, add_feed
from facebook_rss.utils.misc import is_expired_timestamp


def cached(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        feed = get_feed(kwargs['db'], kwargs['profile'])
        if feed and not is_expired_timestamp(feed.timestamp):
            return Response(content=feed.rss, media_type="application/xml")
        value = await func(*args, **kwargs)
        update_feed(
            kwargs['db'], kwargs['profile'], value.body.decode()
        ) if feed else add_feed(kwargs['db'], kwargs['profile'], value.body.decode())
        return value

    return wrapper
