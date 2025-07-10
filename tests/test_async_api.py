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


@pytest.mark.asyncio
async def test_video_search(httpx_mock: HTTPXMock):
    api = pex.AsyncApi("your-api-key")
    response_example = json.load(open(os.path.join(RESPONSES_DIR, "videos_search.json")))

    # Mock the video search endpoint - similar to photos but different endpoint
    httpx_mock.add_response(
        url=f"{HOST}/videos/search?query=nature&orientation=&size=&locale=&per_page=80&page=1",
        json=response_example,
        status_code=200,
    )

    api.videos._host = HOST  # Set host on the videos API object
    results = await api.videos.search("nature", limit=1)
    assert len(results) == len(response_example["videos"])
    result = results[0]
    assert isinstance(result, pex.Video)


@pytest.mark.asyncio
async def test_video_popular(httpx_mock: HTTPXMock):
    api = pex.AsyncApi("your-api-key")
    response_example = json.load(open(os.path.join(RESPONSES_DIR, "videos_popular.json")))

    # Mock the popular videos endpoint - it uses optional dimension/duration params
    httpx_mock.add_response(
        url=f"{HOST}/videos/popular?min_width=&min_height=&min_duration=&max_duration=&per_page=80&page=1",
        json=response_example,
        status_code=200,
    )

    api.videos._host = HOST  # Set host on the videos API object
    results = await api.videos.popular(limit=1)
    assert len(results) == len(response_example["videos"])
    result = results[0]
    assert isinstance(result, pex.Video)


@pytest.mark.asyncio
async def test_video_get(httpx_mock: HTTPXMock):
    api = pex.AsyncApi("your-api-key")
    response_example = json.load(open(os.path.join(RESPONSES_DIR, "video.json")))

    # Mock the get video endpoint - no pagination, just video ID in URL
    video_id = 7438482
    httpx_mock.add_response(
        url=f"{HOST}/videos/videos/{video_id}",
        json=response_example,
        status_code=200,
    )

    api.videos._host = HOST  # Set host on the videos API object
    result = await api.videos.get(video_id)
    assert isinstance(result, pex.Video)
    assert result.id == response_example["id"]


@pytest.mark.asyncio
async def test_collection_featured(httpx_mock: HTTPXMock):
    api = pex.AsyncApi("your-api-key")
    response_example = json.load(open(os.path.join(RESPONSES_DIR, "collections_featured.json")))

    # Mock the featured collections endpoint - it uses empty params with pagination
    httpx_mock.add_response(
        url=f"{HOST}/v1/collections/featured?per_page=80&page=1",
        json=response_example,
        status_code=200,
    )

    api.collections._host = HOST  # Set host on the collections API object
    results = await api.collections.featured(limit=1)
    assert len(results) == len(response_example["collections"])
    result = results[0]
    assert isinstance(result, pex.Collection)


@pytest.mark.asyncio
async def test_collection_my(httpx_mock: HTTPXMock):
    api = pex.AsyncApi("your-api-key")
    response_example = json.load(open(os.path.join(RESPONSES_DIR, "collections_my.json")))

    # Mock the my collections endpoint - it uses empty params with pagination
    httpx_mock.add_response(
        url=f"{HOST}/v1/collections?per_page=80&page=1",
        json=response_example,
        status_code=200,
    )

    api.collections._host = HOST  # Set host on the collections API object
    results = await api.collections.my(limit=1)
    assert len(results) == len(response_example["collections"])
    result = results[0]
    assert isinstance(result, pex.Collection)


@pytest.mark.asyncio
async def test_collection_media(httpx_mock: HTTPXMock):
    api = pex.AsyncApi("your-api-key")
    response_example = json.load(open(os.path.join(RESPONSES_DIR, "collection_media.json")))

    # Mock the collection media endpoint - uses collection ID in URL with optional params
    collection_id = "abc123"
    httpx_mock.add_response(
        url=f"{HOST}/v1/collections/{collection_id}?type=&sort=&per_page=80&page=1",
        json=response_example,
        status_code=200,
    )

    api.collections._host = HOST  # Set host on the collections API object
    results = await api.collections.media(collection_id)
    assert len(results) == len(response_example["media"])
    # The media endpoint can return both photos and videos, so check the first item
    result = results[0]
    assert isinstance(result, (pex.Photo, pex.Video))
