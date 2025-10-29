from typing import Callable, TypeVar
from anyio import to_thread

T = TypeVar("T")

async def run_db(fn: Callable[[], T]) -> T:
    return await to_thread.run_sync(fn)
