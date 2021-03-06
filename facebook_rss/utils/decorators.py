import logging
from functools import wraps

from fastapi import Response

from facebook_rss.db.curd import get_feed, update_feed, add_feed
from facebook_rss.routes import forbidden, unauthorized
from facebook_rss.utils.misc import is_expired_timestamp


def cached(func):
    logger = logging.getLogger('cache')

    @wraps(func)
    async def wrapper(*args, **kwargs):
        feed = get_feed(kwargs['db'], kwargs['fb_page'])
        if not kwargs['commons'].get('no_cache') and feed and not is_expired_timestamp(
                feed.timestamp, expiration=kwargs['settings'].EXPIRATION_TIME):
            logger.info("Valid cached feed found for %s.", kwargs['fb_page'])
            return Response(content=feed.rss, media_type="application/xml")
        logger.info("No valid cached feed found for %s, getting a new feed...", kwargs['fb_page'])
        value = await func(*args, **kwargs)
        update_feed(
            kwargs['db'], kwargs['fb_page'], value.body.decode()
        ) if feed else add_feed(kwargs['db'], kwargs['fb_page'], value.body.decode())
        logger.info("Feeds cache has been updated.")
        return value

    return wrapper


def requires_login(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not kwargs['settings'].USE_ACCOUNT:
            raise forbidden
        value = await func(*args, **kwargs)
        return value

    return wrapper


def requires_auth(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if kwargs['settings'].USE_KEY and kwargs['settings'].API_KEY:
            if not kwargs.get('commons').get('api_key') \
                    or kwargs.get('commons').get('api_key') != kwargs['settings'].API_KEY:
                raise unauthorized
        value = await func(*args, **kwargs)
        return value

    return wrapper


class Singleton:
    def __init__(self, cls):
        self._wrapped = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self._wrapped(*args, **kwargs)
        return self._instance


def singleton(cls):
    return Singleton(cls)
