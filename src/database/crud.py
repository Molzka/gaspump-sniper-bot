from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from .models import OldName, OldUsername, Profile


async def get_profile(engine, user_id: int):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        result = await session.execute(
            select(Profile).where(Profile.user_id == user_id)
        )
    return result.scalars().first()


async def get_ids(engine) -> List[int]:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        result = await session.execute(select(Profile.user_id))
        return [row for row in result.scalars()]


async def create_profile(engine, user_id: int) -> None:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        exists = await session.scalar(
            select(1).where(Profile.user_id == user_id).limit(1)
        )
        if not exists:
            session.add(Profile(user_id=user_id))
            await session.commit()


async def edit_profile(
    engine,
    user_id: int,
    name: Optional[str] = None,
    username: Optional[str] = None,
) -> None:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        profile = await session.get(Profile, user_id)
        if not profile:
            raise ValueError(f"Profile with user_id {user_id} not found")

        if name is not None:
            profile.name = name
        if username is not None:
            profile.username = username

        await session.commit()


async def update_username_history(engine, user_id: int, new_username: str):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        old_username = OldUsername(user_id=user_id, username=new_username)
        session.add(old_username)
        await session.commit()


async def update_name_history(engine, user_id: int, new_name: str):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        old_name = OldName(user_id=user_id, name=new_name)
        session.add(old_name)
        await session.commit()


async def get_username_history(engine, user_id: int) -> list[tuple[str, datetime]]:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        result = await session.execute(
            select(OldUsername.username, OldUsername.changed_at)
            .where(OldUsername.user_id == user_id)
            .order_by(OldUsername.changed_at)
        )
        return result.all()


async def get_name_history(engine, user_id: int) -> list[tuple[str, datetime]]:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        result = await session.execute(
            select(OldName.name, OldName.changed_at)
            .where(OldName.user_id == user_id)
            .order_by(OldName.changed_at)
        )
        return result.all()
