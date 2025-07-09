from pypexel.async_api.async_api_base import AsyncBaseApi
from pypexel.models.models_photo import Photo


class AsyncPhotosApi(AsyncBaseApi):
    async def search(self, query: str, limit: int) -> list[Photo]:
        url = self._url("v1/search")
        params = {"query": query}
        results = await self._request_with_pagination(
            url=url,
            params=params,
            limit=limit,
            key="photos",
        )

        return [Photo(**photo) for photo in results]
