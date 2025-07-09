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
        """Search for photos based on the query and optional parameters.

        Arguments:
            query (str): The search query.
            limit (int): The maximum number of results to return.
            orientation (Literal["landscape", "portrait", "square"], optional): The orientation of the photos.
            size (Literal["large", "medium", "small"], optional): The size of the photos.
            color (str, optional): The color filter for the photos.
            locale (str, optional): The locale for the search results.
            start_page (int, optional): The page number to start from. Defaults to 1.

        Returns:
            list[Photo]: A list of Photo objects matching the search criteria.

        Examples:
            ```python

            import pypexel as pex

            token = "your_api_token_here"
            api = pex.AsyncApi(token=token)

            photos = await api.photos.search(
                query="nature",
                limit=10,
                orientation="landscape",
                size="large",
                color="blue",
                locale="en-US",
                start_page=1
            )

            for photo in photos:
                print(f"Photo ID: {photo.id}, Photographer: {photo.photographer}, URL: {photo.url}")
            ```
        """
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

    async def curated(self, limit: int, start_page: int = 1) -> list[Photo]:
        """Get a curated list of photos.

        Arguments:
            limit (int): The maximum number of results to return.
            start_page (int, optional): The page number to start from. Defaults to 1.

        Returns:
            list[Photo]: A list of curated Photo objects.

        Examples:
            ```python
            import pypexel as pex

            token = "your_api_token_here"
            api = pex.AsyncApi(token=token)

            photos = await api.photos.curated(
                limit=10,
                start_page=1
            )

            for photo in photos:
                print(f"Photo ID: {photo.id}, Photographer: {photo.photographer}, URL: {photo.url}")
            ```
        """
        url = self._url("v1/curated")

        results = await self._request_with_pagination(
            url=url,
            params={},
            limit=limit,
            key=ApiFields.PHOTOS,
            start_page=start_page,
        )

        return [Photo(**photo) for photo in results]

    async def get(self, photo_id: int) -> Photo:
        """Get a photo by its ID.

        Arguments:
            photo_id (int): The ID of the photo to retrieve.

        Returns:
            Photo: The Photo object with the specified ID.

        Examples:
            ```python
            import pypexel as pex

            token = "your_api_token_here"
            api = pex.AsyncApi(token=token)

            photo = await api.photos.get(photo_id=123456)

            print(f"Photo ID: {photo.id}, Photographer: {photo.photographer}, URL: {photo.url}")
            ```
        """
        url = self._url(f"v1/photos/{photo_id}")
        response = await self._request_with_retry(url=url, params={})
        response_data = response.json()
        return Photo(**response_data)
