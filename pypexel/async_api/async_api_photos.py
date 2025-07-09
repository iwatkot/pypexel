from pypexel.async_api.async_api_base import AsyncBaseApi, ApiFields
from pypexel.models.models_photo import Photo

from typing import Literal


class AsyncPhotosApi(AsyncBaseApi):
    key = "photos"

    async def search(
        self,
        query: str,
        limit: int,
        orientation: Literal["landscape", "portrait", "square"] | None = None,
        size: Literal["large", "medium", "small"] | None = None,
        color: str | None = None,
        locale: str | None = None,
        start_page: int = 1,
    ) -> list[Photo]:
        url = self._url("v1/search")
        params = {
            ApiFields.QUERY: query,
            ApiFields.ORIENTATION: orientation,
            ApiFields.SIZE: size,
            ApiFields.COLOR: color,
            ApiFields.LOCALE: locale,
        }

        results = await self._request_with_pagination(
            url=url,
            params=params,
            limit=limit,
            key=ApiFields.PHOTOS,
            start_page=start_page,
        )

        return [Photo(**photo) for photo in results]
