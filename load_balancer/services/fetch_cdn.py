from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import CDNHost
from logging import getLogger

logger = getLogger(__name__)


class FetchCDNService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __call__(self, *args, **kwargs) -> str:
        cdn_host = await self.__fetch_cdn()
        await self.__incr_cnd_connected(cdn_host)
        return cdn_host.host

    async def __fetch_cdn(self) -> CDNHost:
        stmt = select(CDNHost).where(CDNHost.is_active == True).order_by(CDNHost.connected)
        cdn_host = (await self.session.scalars(stmt)).first()
        return cdn_host

    async def __incr_cnd_connected(self, cdn: CDNHost) -> None:
        stmt = update(CDNHost).values(connected=cdn.connected + 1)\
               .where(CDNHost.id == cdn.id)\
               .execution_options(synchronize_session="fetch")
        await self.session.execute(stmt)
        await self.session.commit()


