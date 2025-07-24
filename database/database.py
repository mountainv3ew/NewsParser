import asyncio
import logging

from sqlalchemy.exc import InterfaceError, OperationalError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker

from configs import config
from configs.constants import LOCAL_ENV


def get_engine(url: str) -> AsyncEngine:
    return create_async_engine(
        url=url,
        echo=config.ENV == LOCAL_ENV
    )


def get_sessionmaker(db_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=db_engine, autoflush=False, expire_on_commit=False)


db_url = f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
engine = get_engine(db_url)
async_session = get_sessionmaker(engine)


def retry_on_failure(max_retries=2, retry_exceptions=(InterfaceError, OperationalError), delay=1):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except retry_exceptions as e:
                    retries += 1
                    logging.warning(
                        f"Retry {retries}/{max_retries} due to error: {e}")
                    await asyncio.sleep(delay)
            raise Exception(f"Failed after {max_retries} retries")

        return wrapper

    return decorator
