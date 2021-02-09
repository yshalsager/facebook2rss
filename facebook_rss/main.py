import uvicorn
from fastapi import FastAPI

from facebook_rss import local_cookies
from facebook_rss.config import get_settings
from facebook_rss.routes.group import group_router
from facebook_rss.routes.notification import notifications_router
from facebook_rss.routes.page import page_router
from facebook_rss.routes.profile import profile_router

api = FastAPI()
api.include_router(profile_router)
api.include_router(page_router)
api.include_router(group_router)
api.include_router(notifications_router)


@api.on_event("startup")
async def startup_event():
    settings = get_settings()
    if not local_cookies:
        settings.USE_ACCOUNT = False


async def run_api(development_mode=False):
    if development_mode:
        uvicorn.run("facebook_rss.main:api", host="127.0.0.1", port=8080, reload=True, reload_dirs=['facebook_rss/'])
    else:
        uvicorn.run("facebook_rss.main:api", host="127.0.0.1", port=8080)
