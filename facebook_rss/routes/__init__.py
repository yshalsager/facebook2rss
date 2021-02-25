from typing import Optional

from fastapi import HTTPException, Query
from starlette.responses import Response


class XMLResponse(Response):
    media_type = "application/xml"


async def common_parameters(
        api_key: Optional[str] = Query(None, description="API Key"),
        site: Optional[str] = Query(None, description="site to use (main/mbasic/mobile)",
                                    regex="^main|mbasic|mobile$"),
        full=Query(0, description="Get all recent posts."),
        no_cache=Query(0, description="Ignore cached feed."),
        limit=Query(0, description="Maximum number of posts to fetch."),
        as_text=Query(0, description="Get post content as text instead of HTML."),
        comments=Query(0, description="Include post comments in the feed.")) -> dict:
    return {
        "api_key": api_key,
        "site": site,
        "full": int(full),
        "no_cache": int(no_cache),
        "limit": int(limit),
        "as_text": int(as_text),
        "comments": int(comments)
    }


async def minimal_parameters(
        api_key=Query("", description="API Key"),
        site: Optional[str] = Query(None, description="site to use (main/mbasic/mobile)",
                                    regex="^main|mbasic|mobile$"),
        no_cache=Query(1, description="Ignore cached feed.")) -> dict:
    return {
        "api_key": api_key,
        "site": site,
        "no_cache": int(no_cache)
    }


forbidden = HTTPException(
    status_code=403,
    detail="You cannot access Facebook profiles without enabling USE_ACCOUNT option and logged in.")

unauthorized = HTTPException(
    status_code=401,
    detail="No API Key or wrong key has been provided!")

unavailable = HTTPException(
    status_code=404,
    detail="You cannot access this Facebook url currently. You may checkout what's wrong with it manually.")
