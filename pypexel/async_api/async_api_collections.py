"""This module provides the asynchronous API client for collections."""

from typing import Literal

from pypexel.async_api.async_api_base import ApiFields, AsyncBaseApi
from pypexel.models.models_collection import Collection
from pypexel.models.models_photo import Photo
from pypexel.models.models_video import Video


class AsyncCollectionsApi(AsyncBaseApi):
    async def featured(self, limit: int, start_page: int = 1) -> list[Collection]:
        """Get featured collections.

        Arguments:
            limit (int): The maximum number of collections to return.
            start_page (int): The page number to start from (default is 1).

        Returns:
            list[Collection]: A list of Collection objects representing the featured collections.

        Examples:
            ```python
            import pypexel as pex

            token = "your_api_token_here"
            api = pex.AsyncApi(token=token)

            collections = await api.collections.featured(limit=10, start_page=1)

            for collection in collections:
                print(f"Collection ID: {collection.id}, Title: {collection.title}, Media Count: {collection.media_count}")
            ```
        """
        url = self._url("v1/collections/featured")

        results = await self._request_with_pagination(
            url=url,
            params={},
            limit=limit,
            key=ApiFields.COLLECTIONS,
            start_page=start_page,
        )

        return [Collection(**collection) for collection in results]

    async def my(self, limit: int, start_page: int = 1) -> list[Collection]:
        """Get the user's collections.

        Arguments:
            limit (int): The maximum number of collections to return.
            start_page (int): The page number to start from (default is 1).

        Returns:
            list[Collection]: A list of Collection objects representing the user's collections.

        Examples:
            ```python
            import pypexel as pex

            token = "your_api_token_here"
            api = pex.AsyncApi(token=token)

            collections = await api.collections.my(limit=10, start_page=1)

            for collection in collections:
                print(f"Collection ID: {collection.id}, Title: {collection.title}, Media Count: {collection.media_count}")
            ```
        """
        url = self._url("v1/collections")

        results = await self._request_with_pagination(
            url=url,
            params={},
            limit=limit,
            key=ApiFields.COLLECTIONS,
            start_page=start_page,
        )

        return [Collection(**collection) for collection in results]

    async def media(
        self,
        collection_id: str,
        type: Literal["photos", "videos"] | None = None,
        sort: Literal["asc", "desc"] | None = None,
        start_page: int = 1,
    ) -> list[Photo | Video]:
        """Get media items in a collection.

        Arguments:
            collection_id (str): The ID of the collection to retrieve media from.
            type (Literal["photos", "videos"] | None): The type of media to filter by (default is None, which returns both).
            sort (Literal["asc", "desc"] | None): The sort order for the media items (default is None).
            start_page (int): The page number to start from (default is 1).

        Returns:
            list[Photo | Video]: A list of Photo or Video objects representing the media items in the collection.

        Examples:
            ```python
            import pypexel as pex

            token = "your_api_token_here"
            api = pex.AsyncApi(token=token)

            media_items = await api.collections.media(collection_id="your_collection_id_here")
            for item in media_items:
                if isinstance(item, pex.Photo):
                    print(f"Photo ID: {item.id}, Photographer: {item.photographer}, URL: {item.url}")
                elif isinstance(item, pex.Video):
                    print(f"Video ID: {item.id}, URL: {item.url}, Duration: {item.duration} seconds")
            ```

        """
        url = self._url(f"v1/collections/{collection_id}")

        params = {
            ApiFields.TYPE: type,
            ApiFields.SORT: sort,
        }

        results = await self._request_with_pagination(
            url=url,
            params=params,
            limit=100,
            key=ApiFields.MEDIA,
            start_page=start_page,
        )

        if not results:
            return []

        parsed_results = []
        for item in results:
            if item.get("type") == ApiFields.TYPE_PHOTO:
                parsed_results.append(Photo(**item))
            elif item.get("type") == ApiFields.TYPE_VIDEO:
                parsed_results.append(Video(**item))

        return parsed_results
