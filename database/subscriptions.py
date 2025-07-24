from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert

from database.database import AsyncSession
from models.db.Subscripiton import ChannelSubscription


async def get_all_subscribed_channels(session: AsyncSession) -> list[str]:
    query = (
        select(ChannelSubscription.channel)
        .distinct()
    )

    result = (await session.execute(query)).scalars().all()
    return result


async def get_all_subscriptions(session: AsyncSession) -> list[ChannelSubscription]:
    query = (
        select(ChannelSubscription)
    )

    result = (await session.execute(query)).scalars().all()
    return result


async def add_subscriptions(session: AsyncSession, user_id: int, channels: str):
    subs = [{"user_id": user_id, "channel": channel} for channel in channels]

    query = (
        insert(ChannelSubscription)
        .values(subs)
        .on_conflict_do_nothing(index_elements=["user_id", "channel"])
    )

    await session.execute(query)


async def del_subscriptions(session: AsyncSession, user_id: int, channels: str):
    query = (
        delete(ChannelSubscription)
        .where(ChannelSubscription.user_id == user_id)
        .where(ChannelSubscription.channel.in_(channels))
    )

    await session.execute(query)


async def get_user_subscriptions(session: AsyncSession, user_id: int):
    query = (
        select(ChannelSubscription)
        .where(ChannelSubscription.user_id == user_id)
    )
    
    result = (await session.execute(query)).scalars().all()
    
    return result
