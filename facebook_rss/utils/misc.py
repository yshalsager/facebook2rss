from asyncio import sleep
from random import randint


async def random_sleep():
    await sleep(randint(3, 8))
