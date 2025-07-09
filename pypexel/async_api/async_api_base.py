"""This module provides the base class for asynchronous API clients."""

from typing import Any
import httpx
import asyncio


class AsyncBaseApi:
    """Base class for asynchronous API clients."""

    def __init__(self, token: str, max_retries: int = 3, logger: Any | None = None):
        self._token = token
        self._max_retries = max_retries
        self.logger = logger if logger else Logger(__name__)

        self._host = "https://api.pexels.com"

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
        params: dict[str, str],
        limit: int,
        key: str,
        method: str = "GET",
        start_page: int = 1,
    ) -> list:
        """Makes an asynchronous HTTP request with pagination.

        Arguments:
            url (str): The URL to request.
            params (dict[str, str]): The query parameters for the request.
            limit (int): The maximum number of results to return.
            key (str): The key in the response JSON that contains the results.
            method (str): The HTTP method to use ('GET' or 'POST').
            start_page (int): The page number to start from (default is 1).

        Returns:
            list: A list of results from the API response.
        """
        params["per_page"] = 80  # Using maximum allowed by Pexels API.
        params["page"] = start_page

        results = []
        while len(results) < limit:
            response = await self._request_with_retry(url, params, method)
            data = response.json()

            if key not in data:
                raise ValueError(f"Key {key} not found in the response.")

            results.extend(data[key])

            params["page"] += 1

        return results[:limit]

    async def _request_with_retry(
        self, url: str, params: dict[str, str], method: str = "GET"
    ) -> httpx.Response:
        """Makes an asynchronous HTTP request with retry logic.

        Arguments:
            url (str): The URL to request.
            params (dict[str, str]): The query parameters for the request.
            method (str): The HTTP method to use ('GET' or 'POST').

        Returns:
            httpx.Response: The response from the HTTP request.

        Raises:
            ValueError: If the method is not 'GET' or 'POST'.
            httpx.RequestError: If there is a network-related error.
            httpx.TimeoutException: If the request times out.
            httpx.HTTPStatusError: If the response status code indicates an error.
            ConnectionError: If the maximum number of retries is exceeded.
        """
        self.logger.debug("Making %s request to %s...", method, url)
        for retry in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient() as client:
                    if method == "GET":
                        func = client.get
                    elif method == "POST":
                        func = client.post
                    else:
                        raise ValueError(
                            "Unsupported HTTP method. Use 'GET' or 'POST'."
                        )

                    response = await func(
                        url, headers={"Authorization": self._token}, params=params
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

        raise ConnectionError(
            f"Max retries exceeded with no successful response to {url}"
        )


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
