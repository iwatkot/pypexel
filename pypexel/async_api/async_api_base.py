"""This module provides the base class for asynchronous API clients."""

import asyncio
from typing import Any

import httpx


class ApiFields:
    PHOTOS = "photos"
    VIDEOS = "videos"
    COLLECTIONS = "collections"
    MEDIA = "media"

    QUERY = "query"
    ORIENTATION = "orientation"
    SIZE = "size"
    COLOR = "color"
    LOCALE = "locale"

    MIN_WIDTH = "min_width"
    MIN_HEIGHT = "min_height"
    MIN_DURATION = "min_duration"
    MAX_DURATION = "max_duration"

    TOTAL_RESULTS = "total_results"

    TYPE = "type"
    TYPE_PHOTO = "Photo"
    TYPE_VIDEO = "Video"
    SORT = "sort"


class AsyncBaseApi:
    """Base class for asynchronous API clients."""

    def __init__(
        self,
        token: str,
        max_retries: int = 3,
        logger: Any | None = None,
        timeout: int = 30,
    ):
        self._token = token
        self._max_retries = max_retries
        self.logger = logger if logger is not None else Logger(__name__)

        self._host = "https://api.pexels.com"
        self._timeout = timeout

    @property
    def token(self) -> str:
        """Returns the API token.

        Returns:
            str: The API token.
        """
        return self._token

    @property
    def max_retries(self) -> int:
        """Returns the maximum number of retries for API requests.

        Returns:
            int: The maximum number of retries.
        """
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value: int) -> None:
        """Sets the maximum number of retries for API requests.

        Arguments:
            value (int): The maximum number of retries.

        Raises:
            ValueError: If the value is not a positive integer.
        """
        if not isinstance(value, int) or value < 1:
            raise ValueError("max_retries must be a positive integer.")
        self._max_retries = value

    def _url(self, endpoint: str) -> str:
        """Returns the URL for API (adds the endpoint to the host URL).

        Arguments:
            endpoint (str): The endpoint for the API.

        Returns:
            str: The URL for the API.
        """
        return f"{self._host}/{endpoint}"

    async def _request_with_pagination(
        self,
        url: str,
        params: dict[str, str | int | None],
        limit: int,
        key: str,
        start_page: int = 1,
    ) -> list[Any]:
        """Makes an asynchronous HTTP request with pagination.

        Arguments:
            url (str): The URL to request.
            params (dict[str, str | int | None]): The query parameters for the request.
            limit (int): The maximum number of results to return.
            key (str): The key in the response JSON that contains the results.
            start_page (int): The page number to start from (default is 1).

        Returns:
            list: A list of results from the API response.
        """
        params["per_page"] = 80  # Using maximum allowed by Pexels API.
        params["page"] = start_page

        self.logger.debug(
            "Starting pagination with URL: %s, params: %s, limit: %d, key: %s",
            url,
            params,
            limit,
            key,
        )

        results: list[Any] = []
        while len(results) < limit:
            response = await self._request_with_retry(url, params)
            data = response.json()

            if key not in data:
                raise ValueError(f"Key {key} not found in the response.")

            results.extend(data[key])

            params["page"] += 1  # type: ignore

            if data.get(ApiFields.TOTAL_RESULTS, 0) < limit:
                self.logger.debug(
                    "Total results (%d) less than limit (%d), stopping pagination.",
                    data.get(ApiFields.TOTAL_RESULTS, 0),
                    limit,
                )
                break

        return results[:limit]

    async def _request_with_retry(
        self, url: str, params: dict[str, str | int | None]
    ) -> httpx.Response:
        """Makes an asynchronous HTTP request with retry logic.

        Arguments:
            url (str): The URL to request.
            params (dict[str, str]): The query parameters for the request.

        Returns:
            httpx.Response: The response from the HTTP request.

        Raises:
            httpx.RequestError: If there is a network-related error.
            httpx.TimeoutException: If the request times out.
            httpx.HTTPStatusError: If the response status code indicates an error.
            ConnectionError: If the maximum number of retries is exceeded.
        """
        self.logger.debug("Making request to %s...", url)
        for retry in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        url,
                        headers={"Authorization": self._token},
                        params=params,
                        timeout=self._timeout,
                    )
                    response.raise_for_status()

                    return response
            except (httpx.RequestError, httpx.TimeoutException) as e:
                if retry == self.max_retries:
                    raise e
                self.logger.warning(
                    "Request failed on attempt %d/%d: %s",
                    retry,
                    self.max_retries,
                    str(e),
                )
                await asyncio.sleep(1 * (retry + 1))
            except httpx.HTTPStatusError as e:
                raise e

        raise ConnectionError(f"Max retries exceeded with no successful response to {url}")


class Logger:
    """Dummy logger class for compatibility.
    Does not perform any logging operations.
    """

    def __init__(self, name: str):
        pass

    def debug(self, *args, **kwargs) -> None:
        pass

    def info(self, *args, **kwargs) -> None:
        pass

    def warning(self, *args, **kwargs) -> None:
        pass

    def error(self, *args, **kwargs) -> None:
        pass
