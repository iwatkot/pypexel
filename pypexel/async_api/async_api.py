"""This module provides the main class for asynchronous API clients."""

from typing import Any

from pypexel.async_api.async_api_photos import AsyncPhotosApi
from pypexel.async_api.async_api_videos import AsyncVideosApi


class AsyncApi:
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
