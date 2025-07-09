"""This module provides the main class for asynchronous API clients."""

from __future__ import annotations

import os
from typing import Any

from pypexel.async_api.async_api_collections import AsyncCollectionsApi
from pypexel.async_api.async_api_photos import AsyncPhotosApi
from pypexel.async_api.async_api_videos import AsyncVideosApi


class AsyncApi:
    """Main class for asynchronous API clients.
    This class provides access to the Pexels API for photos, videos, and collections.

    Arguments:
        token (str): The API token for authentication.
        max_retries (int): The maximum number of retries for API requests (default is 3).
        logger (Any | None): An optional logger instance for logging (default is None).
        timeout (int): The timeout for API requests in seconds (default is 30).

    Attributes:
        photos (AsyncPhotosApi): An instance of AsyncPhotosApi for accessing photo-related endpoints.
        videos (AsyncVideosApi): An instance of AsyncVideosApi for accessing video-related endpoints.
        collections (AsyncCollectionsApi): An instance of AsyncCollectionsApi for accessing collection-related endpoints.

    Methods:
        from_env(): Creates an AsyncApi instance from environment variables.

    Examples:
        ```python
        import os
        import pypexel as pex

        # Create an AsyncApi instance using the API token
        api = pex.AsyncApi(token="YOUR_API_TOKEN")

        # Create an AsyncApi instance from environment variables
        os.environ["PEXELS_API_KEY"] = "YOUR_API_TOKEN"
        api = pex.AsyncApi.from_env()

        # Access photos, videos, and collections
        photos = await api.photos.search("nature", limit=10)
        videos = await api.videos.popular(limit=5)
        collections = await api.collections.featured(limit=3)
        ```
    """

    def __init__(
        self,
        token: str,
        max_retries: int = 3,
        logger: Any | None = None,
        timeout: int = 30,
    ):
        self.photos = AsyncPhotosApi(
            token=token, max_retries=max_retries, logger=logger, timeout=timeout
        )
        self.videos = AsyncVideosApi(
            token=token, max_retries=max_retries, logger=logger, timeout=timeout
        )
        self.collections = AsyncCollectionsApi(
            token=token, max_retries=max_retries, logger=logger, timeout=timeout
        )

    @classmethod
    def from_env(
        cls, max_retries: int = 3, logger: Any | None = None, timeout: int = 30
    ) -> AsyncApi:
        """Create an AsyncApi instance from environment variables.
        Uses the following environment variable:
            - PEXELS_API_KEY: The API key for Pexels API.

        Arguments:
            max_retries (int): The maximum number of retries for API requests (default is 3).
            logger (Any | None): An optional logger instance for logging (default is None).
            timeout (int): The timeout for API requests in seconds (default is 30).

        Returns:
            AsyncApi: An instance of AsyncApi initialized with the PEXELS_API_KEY from environment variables.

        Raises:
            ValueError: If the PEXELS_API_KEY environment variable is not set.
        """

        token = os.getenv("PEXELS_API_KEY")
        if not token:
            raise ValueError("PEXELS_API_KEY environment variable is not set.")

        return cls(token=token, max_retries=max_retries, logger=logger)
