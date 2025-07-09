<a id="async_api.async_api"></a>

# async\_api.async\_api

This module provides the main class for asynchronous API clients.

<a id="async_api.async_api.AsyncApi"></a>

## AsyncApi Objects

```python
class AsyncApi()
```

Main class for asynchronous API clients.
This class provides access to the Pexels API for photos, videos, and collections.

**Arguments**:

- `token` _str_ - The API token for authentication.
- `max_retries` _int_ - The maximum number of retries for API requests (default is 3).
- `logger` _Any | None_ - An optional logger instance for logging (default is None).
- `timeout` _int_ - The timeout for API requests in seconds (default is 30).
  

**Attributes**:

- `photos` _AsyncPhotosApi_ - An instance of AsyncPhotosApi for accessing photo-related endpoints.
- `videos` _AsyncVideosApi_ - An instance of AsyncVideosApi for accessing video-related endpoints.
- `collections` _AsyncCollectionsApi_ - An instance of AsyncCollectionsApi for accessing collection-related endpoints.
  

**Methods**:

- `from_env()` - Creates an AsyncApi instance from environment variables.
  

**Examples**:

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

<a id="async_api.async_api.AsyncApi.from_env"></a>

#### from\_env

```python
@classmethod
def from_env(cls,
             max_retries: int = 3,
             logger: Any | None = None,
             timeout: int = 30) -> AsyncApi
```

Create an AsyncApi instance from environment variables.
Uses the following environment variable:
- PEXELS_API_KEY: The API key for Pexels API.

**Arguments**:

- `max_retries` _int_ - The maximum number of retries for API requests (default is 3).
- `logger` _Any | None_ - An optional logger instance for logging (default is None).
- `timeout` _int_ - The timeout for API requests in seconds (default is 30).
  

**Returns**:

- `AsyncApi` - An instance of AsyncApi initialized with the PEXELS_API_KEY from environment variables.
  

**Raises**:

- `ValueError` - If the PEXELS_API_KEY environment variable is not set.

<a id="async_api.async_api_base"></a>

# async\_api.async\_api\_base

This module provides the base class for asynchronous API clients.

<a id="async_api.async_api_base.ApiFields"></a>

## ApiFields Objects

```python
class ApiFields()
```

Constants for API fields used in requests and responses.

<a id="async_api.async_api_base.AsyncBaseApi"></a>

## AsyncBaseApi Objects

```python
class AsyncBaseApi()
```

Base class for asynchronous API clients.

<a id="async_api.async_api_base.AsyncBaseApi.token"></a>

#### token

```python
@property
def token() -> str
```

Returns the API token.

**Returns**:

- `str` - The API token.

<a id="async_api.async_api_base.AsyncBaseApi.max_retries"></a>

#### max\_retries

```python
@property
def max_retries() -> int
```

Returns the maximum number of retries for API requests.

**Returns**:

- `int` - The maximum number of retries.

<a id="async_api.async_api_base.AsyncBaseApi.max_retries"></a>

#### max\_retries

```python
@max_retries.setter
def max_retries(value: int) -> None
```

Sets the maximum number of retries for API requests.

**Arguments**:

- `value` _int_ - The maximum number of retries.
  

**Raises**:

- `ValueError` - If the value is not a positive integer.

<a id="async_api.async_api_base.Logger"></a>

## Logger Objects

```python
class Logger()
```

Dummy logger class for compatibility.
Does not perform any logging operations.

<a id="async_api.async_api_base.Logger.debug"></a>

#### debug

```python
def debug(*args, **kwargs) -> None
```

Dummy debug method that does nothing.

<a id="async_api.async_api_base.Logger.info"></a>

#### info

```python
def info(*args, **kwargs) -> None
```

Dummy info method that does nothing.

<a id="async_api.async_api_base.Logger.warning"></a>

#### warning

```python
def warning(*args, **kwargs) -> None
```

Dummy warning method that does nothing.

<a id="async_api.async_api_base.Logger.error"></a>

#### error

```python
def error(*args, **kwargs) -> None
```

Dummy error method that does nothing.

<a id="async_api.async_api_collections"></a>

# async\_api.async\_api\_collections

This module provides the asynchronous API client for collections.

<a id="async_api.async_api_collections.AsyncCollectionsApi"></a>

## AsyncCollectionsApi Objects

```python
class AsyncCollectionsApi(AsyncBaseApi)
```

Asynchronous API client for collections.

<a id="async_api.async_api_collections.AsyncCollectionsApi.featured"></a>

#### featured

```python
async def featured(limit: int, start_page: int = 1) -> list[Collection]
```

Get featured collections.

**Arguments**:

- `limit` _int_ - The maximum number of collections to return.
- `start_page` _int_ - The page number to start from (default is 1).
  

**Returns**:

- `list[Collection]` - A list of Collection objects representing the featured collections.
  

**Examples**:

    ```python
    import pypexel as pex

    token = "your_api_token_here"
    api = pex.AsyncApi(token=token)

    collections = await api.collections.featured(limit=10, start_page=1)

    for collection in collections:
        print(f"Collection ID: {collection.id}, Title: {collection.title}, Media Count: {collection.media_count}")
    ```

<a id="async_api.async_api_collections.AsyncCollectionsApi.my"></a>

#### my

```python
async def my(limit: int, start_page: int = 1) -> list[Collection]
```

Get the user's collections.

**Arguments**:

- `limit` _int_ - The maximum number of collections to return.
- `start_page` _int_ - The page number to start from (default is 1).
  

**Returns**:

- `list[Collection]` - A list of Collection objects representing the user's collections.
  

**Examples**:

    ```python
    import pypexel as pex

    token = "your_api_token_here"
    api = pex.AsyncApi(token=token)

    collections = await api.collections.my(limit=10, start_page=1)

    for collection in collections:
        print(f"Collection ID: {collection.id}, Title: {collection.title}, Media Count: {collection.media_count}")
    ```

<a id="async_api.async_api_collections.AsyncCollectionsApi.media"></a>

#### media

```python
async def media(collection_id: str,
                media_type: Literal["photos", "videos"] | None = None,
                sort: Literal["asc", "desc"] | None = None,
                start_page: int = 1) -> list[Photo | Video]
```

Get media items in a collection.

**Arguments**:

- `collection_id` _str_ - The ID of the collection to retrieve media from.
- `media_type` _Literal["photos", "videos"] | None_ - The type of media to filter by (default is None, which returns both).
- `sort` _Literal["asc", "desc"] | None_ - The sort order for the media items (default is None).
- `start_page` _int_ - The page number to start from (default is 1).
  

**Returns**:

  list[Photo | Video]: A list of Photo or Video objects representing the media items in the collection.
  

**Examples**:

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

<a id="async_api.async_api_photos"></a>

# async\_api.async\_api\_photos

This module provides an asynchronous API client for searching and retrieving photos from the Pexels API.

<a id="async_api.async_api_photos.AsyncPhotosApi"></a>

## AsyncPhotosApi Objects

```python
class AsyncPhotosApi(AsyncBaseApi)
```

Asynchronous API client for photos.

<a id="async_api.async_api_photos.AsyncPhotosApi.search"></a>

#### search

```python
async def search(query: str,
                 limit: int,
                 orientation: Literal["landscape", "portrait", "square"]
                 | None = None,
                 size: Literal["large", "medium", "small"] | None = None,
                 color: str | None = None,
                 locale: str | None = None,
                 start_page: int = 1) -> list[Photo]
```

Search for photos based on the query and optional parameters.

**Arguments**:

- `query` _str_ - The search query.
- `limit` _int_ - The maximum number of results to return.
- `orientation` _Literal["landscape", "portrait", "square"], optional_ - The orientation of the photos.
- `size` _Literal["large", "medium", "small"], optional_ - The size of the photos.
- `color` _str, optional_ - The color filter for the photos.
- `locale` _str, optional_ - The locale for the search results.
- `start_page` _int, optional_ - The page number to start from. Defaults to 1.
  

**Returns**:

- `list[Photo]` - A list of Photo objects matching the search criteria.
  

**Examples**:

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

<a id="async_api.async_api_photos.AsyncPhotosApi.curated"></a>

#### curated

```python
async def curated(limit: int, start_page: int = 1) -> list[Photo]
```

Get a curated list of photos.

**Arguments**:

- `limit` _int_ - The maximum number of results to return.
- `start_page` _int, optional_ - The page number to start from. Defaults to 1.
  

**Returns**:

- `list[Photo]` - A list of curated Photo objects.
  

**Examples**:

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

<a id="async_api.async_api_photos.AsyncPhotosApi.get"></a>

#### get

```python
async def get(photo_id: int) -> Photo
```

Get a photo by its ID.

**Arguments**:

- `photo_id` _int_ - The ID of the photo to retrieve.
  

**Returns**:

- `Photo` - The Photo object with the specified ID.
  

**Examples**:

    ```python
    import pypexel as pex

    token = "your_api_token_here"
    api = pex.AsyncApi(token=token)

    photo = await api.photos.get(photo_id=123456)

    print(f"Photo ID: {photo.id}, Photographer: {photo.photographer}, URL: {photo.url}")
    ```

<a id="async_api.async_api_videos"></a>

# async\_api.async\_api\_videos

This module provides the asynchronous API client for videos.

<a id="async_api.async_api_videos.AsyncVideosApi"></a>

## AsyncVideosApi Objects

```python
class AsyncVideosApi(AsyncBaseApi)
```

Asynchronous API client for videos.

<a id="async_api.async_api_videos.AsyncVideosApi.search"></a>

#### search

```python
async def search(query: str,
                 limit: int,
                 orientation: Literal["landscape", "portrait", "square"]
                 | None = None,
                 size: Literal["large", "medium", "small"] | None = None,
                 locale: str | None = None,
                 start_page: int = 1) -> list[Video]
```

Search for videos based on the query and optional parameters.

**Arguments**:

- `query` _str_ - The search query.
- `limit` _int_ - The maximum number of results to return.
- `orientation` _Literal["landscape", "portrait", "square"], optional_ - The orientation of the videos.
- `size` _Literal["large", "medium", "small"], optional_ - The size of the videos.
- `locale` _str, optional_ - The locale for the search results.
- `start_page` _int, optional_ - The page number to start from. Defaults to 1.
  

**Returns**:

- `list[Video]` - A list of Video objects matching the search criteria.
  

**Examples**:

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

<a id="async_api.async_api_videos.AsyncVideosApi.popular"></a>

#### popular

```python
async def popular(limit: int,
                  min_width: int | None = None,
                  min_height: int | None = None,
                  min_duration: int | None = None,
                  max_duration: int | None = None,
                  start_page: int = 1) -> list[Video]
```

Get a list of popular videos.

**Arguments**:

- `limit` _int_ - The maximum number of results to return.
- `min_width` _int, optional_ - Minimum width of the videos.
- `min_height` _int, optional_ - Minimum height of the videos.
- `min_duration` _int, optional_ - Minimum duration of the videos in seconds.
- `max_duration` _int, optional_ - Maximum duration of the videos in seconds.
- `start_page` _int, optional_ - The page number to start from. Defaults to 1.
  

**Returns**:

- `list[Video]` - A list of popular Video objects.
  

**Examples**:

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

<a id="async_api.async_api_videos.AsyncVideosApi.get"></a>

#### get

```python
async def get(video_id: int) -> Video
```

Get a video by its ID.

**Arguments**:

- `video_id` _int_ - The ID of the video to retrieve.
  

**Returns**:

- `Video` - The Video object with the specified ID.
  

**Examples**:

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

