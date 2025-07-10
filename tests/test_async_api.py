import json
import os

import pytest
from pytest_httpx import HTTPXMock

import pypexel as pex

RESPONSES_DIR = "tests/responses"
HOST = "http://localhost"


@pytest.mark.asyncio
async def test_from_env():
    os.environ["PEXELS_API_KEY"] = "your-api-key"
    api = pex.AsyncApi.from_env()
    assert api.photos.token == "your-api-key"


@pytest.mark.asyncio
async def test_from_env_failed():
    # Remove the environment variable to test failure.
    # from_env() should raise ValueError if PEXELS_API_KEY is not set.
    if "PEXELS_API_KEY" in os.environ:
        del os.environ["PEXELS_API_KEY"]
    with pytest.raises(ValueError):
        pex.AsyncApi.from_env()


@pytest.mark.asyncio
async def test_photo_search(httpx_mock: HTTPXMock):
    api = pex.AsyncApi("your-api-key")
    response_example = json.load(open(os.path.join(RESPONSES_DIR, "photos_search.json")))

    # Mock the exact request URL including the empty parameters
    httpx_mock.add_response(
        url=f"{HOST}/v1/search?query=nature&orientation=&size=&color=&locale=&per_page=80&page=1",
        json=response_example,
        status_code=200,
    )

    api.photos._host = HOST  # Set host on the photos API object
    results = await api.photos.search("nature", limit=1)
    assert len(results) == len(response_example["photos"])
    result = results[0]
    assert isinstance(result, pex.Photo)


@pytest.mark.asyncio
async def test_photo_curated(httpx_mock: HTTPXMock):
    api = pex.AsyncApi("your-api-key")
    response_example = json.load(open(os.path.join(RESPONSES_DIR, "photos_curated.json")))

    # Mock the curated endpoint - it uses empty params with pagination
    httpx_mock.add_response(
        url=f"{HOST}/v1/curated?per_page=80&page=1",
        json=response_example,
        status_code=200,
    )

    api.photos._host = HOST  # Set host on the photos API object
    results = await api.photos.curated(limit=5)
    assert len(results) == len(response_example["photos"])
    result = results[0]
    assert isinstance(result, pex.Photo)


@pytest.mark.asyncio
async def test_photo_get(httpx_mock: HTTPXMock):
    api = pex.AsyncApi("your-api-key")
    response_example = json.load(open(os.path.join(RESPONSES_DIR, "photo.json")))

    # Mock the get photo endpoint - no pagination, just photo ID in URL
    photo_id = 12345678
    httpx_mock.add_response(
        url=f"{HOST}/v1/photos/{photo_id}",
        json=response_example,
        status_code=200,
    )

    api.photos._host = HOST  # Set host on the photos API object
    result = await api.photos.get(photo_id)
    assert isinstance(result, pex.Photo)
    assert result.id == response_example["id"]
