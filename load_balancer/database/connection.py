from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from load_balancer.config import LoadBalancerConfig


engine = create_async_engine(LoadBalancerConfig.DATABASE_URI)

Session = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, autocommit=False)

Base = declarative_base()
Base.query = Session().query_property()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session


async def init_db():
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


