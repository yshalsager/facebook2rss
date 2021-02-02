from asyncio import sleep
from datetime import datetime, timedelta
from random import randint


async def random_sleep():
    await sleep(randint(3, 8))


def is_expired_timestamp(timestamp: datetime, expiration=30) -> bool:
    return bool(datetime.utcnow() > timestamp + timedelta(minutes=expiration))
