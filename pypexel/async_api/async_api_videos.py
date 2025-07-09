"""This module provides the asynchronous API client for videos."""

from typing import Literal

from pypexel.async_api.async_api_base import ApiFields, AsyncBaseApi
from pypexel.models.models_video import Video


class AsyncVideosApi(AsyncBaseApi):
    async def search(
        self,
        query: str,
        limit: int,
        orientation: Literal["landscape", "portrait", "square"] | None = None,
        size: Literal["large", "medium", "small"] | None = None,
        locale: str | None = None,
        start_page: int = 1,
    ) -> list[Video]:
        """Search for videos based on the query and optional parameters.

        Arguments:
            query (str): The search query.
            limit (int): The maximum number of results to return.
            orientation (Literal["landscape", "portrait", "square"], optional): The orientation of the videos.
            size (Literal["large", "medium", "small"], optional): The size of the videos.
            locale (str, optional): The locale for the search results.
            start_page (int, optional): The page number to start from. Defaults to 1.

        Returns:
            list[Video]: A list of Video objects matching the search criteria.

        Examples:
            ```python
            import pypexel as pex

            token = "your_api_token_here"
            api = pex.AsyncApi(token=token)

            videos = await api.videos.search(
                query="nature",
                limit=10,
                orientation="landscape",
                size="large",
                locale="en-US",
                start_page=1
            )

            for video in videos:
                print(f"Video ID: {video.id}, URL: {video.url}, Duration: {video.duration} seconds")
                for video_file in video.video_files:
                    print(
                        f"  File: {video_file.file_type}, Quality: {video_file.quality}, Width: {video_file.width}, Height: {video_file.height}"
                    )
            ```
        """
        url = self._url("videos/search")
        params = {
            ApiFields.QUERY: query,
            ApiFields.ORIENTATION: orientation,
            ApiFields.SIZE: size,
            ApiFields.LOCALE: locale,
        }

        results = await self._request_with_pagination(
            url=url,
            params=params,
            limit=limit,
            key=ApiFields.VIDEOS,
            start_page=start_page,
        )

        return [Video(**video) for video in results]

    async def popular(
        self,
        limit: int,
        min_width: int | None = None,
        min_height: int | None = None,
        min_duration: int | None = None,
        max_duration: int | None = None,
        start_page: int = 1,
    ) -> list[Video]:
        """Get a list of popular videos.

        Arguments:
            limit (int): The maximum number of results to return.
            min_width (int, optional): Minimum width of the videos.
            min_height (int, optional): Minimum height of the videos.
            min_duration (int, optional): Minimum duration of the videos in seconds.
            max_duration (int, optional): Maximum duration of the videos in seconds.
            start_page (int, optional): The page number to start from. Defaults to 1.

        Returns:
            list[Video]: A list of popular Video objects.

        Examples:
            ```python
            import pypexel as pex

            token = "your_api_token_here"
            api = pex.AsyncApi(token=token)

            videos = await api.videos.popular(
                limit=10,
                min_width=640,
                min_height=480,
                min_duration=5,
                max_duration=60,
                start_page=1
            )

            for video in videos:
                print(f"Video ID: {video.id}, URL: {video.url}, Duration: {video.duration} seconds")
                for video_file in video.video_files:
                    print(
                        f"  File: {video_file.file_type}, Quality: {video_file.quality}, Width: {video_file.width}, Height: {video_file.height}"
                    )
            ```
        """
        url = self._url("videos/popular")

        params = {
            ApiFields.MIN_WIDTH: min_width,
            ApiFields.MIN_HEIGHT: min_height,
            ApiFields.MIN_DURATION: min_duration,
            ApiFields.MAX_DURATION: max_duration,
        }

        results = await self._request_with_pagination(
            url=url,
            params=params,
            limit=limit,
            key=ApiFields.VIDEOS,
            start_page=start_page,
        )

        return [Video(**video) for video in results]

    async def get(self, video_id: int) -> Video:
        """Get a video by its ID.

        Arguments:
            video_id (int): The ID of the video to retrieve.

        Returns:
            Video: The Video object with the specified ID.

        Examples:
            ```python
            import pypexel as pex

            token = "your_api_token_here"
            api = pex.AsyncApi(token=token)

            video = await api.videos.get(video_id=12345678)
            print(f"Video ID: {video.id}, URL: {video.url}, Duration: {video.duration} seconds")
            for video_file in video.video_files:
                print(
                    f"  File: {video_file.file_type}, Quality: {video_file.quality}, Width: {video_file.width}, Height: {video_file.height}"
                )
            ```
        """
        url = self._url(f"videos/videos/{video_id}")
        response = await self._request_with_retry(url=url, params={})
        response_data = response.json()
        return Video(**response_data)
