from fastapi import HTTPException, Query
from starlette.responses import Response


class XMLResponse(Response):
    media_type = "application/xml"


async def common_parameters(
        full=Query(0, description="Get all recent posts."),
        no_cache=Query(0, description="Ignore cached feed."),
        limit=Query(0, description="Maximum number of posts to fetch."),
        as_text=Query(0, description="Get post content as text instead of HTML."),
        comments=Query(0, description="Include post comments in the feed.")):
    return {
        "full": int(full),
        "no_cache": int(no_cache),
        "limit": int(limit),
        "as_text": int(as_text),
        "comments": int(comments)
    }


unauthorized = HTTPException(
    status_code=403,
    detail="You cannot access Facebook profiles without enabling USE_ACCOUNT option and logged in.")

unavailable = HTTPException(
    status_code=404,
    detail="You cannot access this Facebook url currently. You may checkout what's wrong with it manually")
