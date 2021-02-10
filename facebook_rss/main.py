import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger

from facebook_rss import local_cookies
from facebook_rss.config import get_settings
from facebook_rss.routes import XMLResponse
from facebook_rss.routes.group import group_router
from facebook_rss.routes.notification import notifications_router
from facebook_rss.routes.page import page_router
from facebook_rss.routes.profile import profile_router

tags_metadata = [
    {
        "name": "profiles",
        "description": "Get RSS feed of a Facebook profile **(Requires login)**.",
    }, {
        "name": "pages",
        "description": "Get RSS feed of a Facebook page.",
    }, {
        "name": "groups",
        "description": "Get RSS feed of a Facebook group.",
    }, {
        "name": "notifications",
        "description": "Get RSS feed of your Facebook account notifications **(Requires login)**.",
    }
]

api = FastAPI(
    title="Facebook to RSS",
    description="A simple API to bring back RSS feed of Facebook",
    version="0.3.0",
    openapi_tags=tags_metadata,
    default_response_class=XMLResponse
)
api.include_router(profile_router)
api.include_router(page_router)
api.include_router(group_router)
api.include_router(notifications_router)


@api.on_event("startup")
async def startup_event():
    logger.info("Starting...")
    settings = get_settings()
    if not local_cookies:
        logger.info("Login cookies file was not found, setting working mode to no account!")
        settings.USE_ACCOUNT = False
    logger.info("Login cookies file was found, setting working mode to use account!")


async def run_api(development_mode=False):
    if development_mode:
        logger.info("Running in development mode!")
        uvicorn.run("facebook_rss.main:api", host="127.0.0.1", port=8080, reload=True, reload_dirs=['facebook_rss/'])
    else:
        uvicorn.run("facebook_rss.main:api", host="127.0.0.1", port=8080)
