from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import CDNHost


class FetchCDNService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __call__(self, *args, **kwargs) -> str:
        cdn_host = await self.__fetch_cdn()
        return cdn_host.host

    async def __fetch_cdn(self) -> CDNHost:
        stmt = select(CDNHost).where(CDNHost.is_active == True).order_by(CDNHost.connected)
        cdn_host = (await self.session.scalars(stmt)).first()
        return cdn_host



