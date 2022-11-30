from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from load_balancer.config import LoadBalancerConfig


engine = create_async_engine(LoadBalancerConfig.DATABASE_URI)

Session = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, autocommit=False)

Base = declarative_base()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


