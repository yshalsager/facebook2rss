import uvicorn
from fastapi import FastAPI

from facebook_rss import browser, cookies
from facebook_rss.routes import home
from facebook_rss.utils.misc import unpickle

api = FastAPI()
api.include_router(home.router)


@api.on_event("startup")
async def startup():
    await browser.start(headless=False)
    await browser.add_cookies(unpickle(cookies))


@api.on_event("shutdown")
async def shutdown():
    await browser.shutdown()


async def run_api(development_mode=False):
    if development_mode:
        uvicorn.run("facebook_rss.main:api", host="127.0.0.1", port=8081, reload=True)
    else:
        uvicorn.run("facebook_rss.main:api", host="127.0.0.1", port=8081)
