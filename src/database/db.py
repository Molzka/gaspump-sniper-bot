from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from ..config import DB_PATH as db_path

Base = declarative_base()

engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}")


async def db_start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


def get_engine():
    return engine
