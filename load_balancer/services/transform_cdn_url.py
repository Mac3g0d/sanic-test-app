from urllib.parse import urlparse

from sqlalchemy.ext.asyncio import AsyncSession

from .fetch_cdn import FetchCDNService


class TransformCdnUrlService:
    def __init__(self, video_url: str, session: AsyncSession) -> None:
        self.video_url = video_url
        self.parsed_video_url = urlparse(video_url)
        self.session = session

    async def __call__(self) -> str:
        return await self.transform_url()

    async def transform_url(self) -> str:
        cdn_host = await FetchCDNService(self.session)()
        cdn_origin_server = self.fetch_cdn_origin_server()
        location_path = self.fetch_location_path()
        cdn_hosted_url = f'http://{cdn_host}/{cdn_origin_server}{location_path}'
        return cdn_hosted_url

    def fetch_location_path(self) -> str:
        return self.parsed_video_url.path

    def fetch_cdn_origin_server(self) -> str:
        return self.parsed_video_url.netloc.split('.')[0]


