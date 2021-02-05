import uvicorn
from fastapi import FastAPI

from facebook_rss.routes.profile import profile_router

api = FastAPI()
api.include_router(profile_router)


async def run_api(development_mode=False):
    if development_mode:
        uvicorn.run("facebook_rss.main:api", host="127.0.0.1", port=8081, reload=True)
    else:
        uvicorn.run("facebook_rss.main:api", host="127.0.0.1", port=8081)
