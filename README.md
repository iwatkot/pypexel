<div align="center" markdown>
<img src="">

Async Object-oriented Python SDK for the Pexels API.

<p align="center">
    <a href="#Overview">Overview</a> •
    <a href="#Quick-Start">Quick Start</a> •
    <a href="#Examples">Examples</a> •
    <a href="#Bugs-and-Feature-Requests">Bugs and Feature Requests</a> •
    <a href="https://pypi.org/project/pypexel/">PyPI</a>
</p>

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/iwatkot/pypexel)](https://github.com/iwatkot/pypexel/releases)
[![PyPI - Version](https://img.shields.io/pypi/v/pypexel)](https://pypi.org/project/pypexel/)
[![GitHub issues](https://img.shields.io/github/issues/iwatkot/pypexel)](https://github.com/iwatkot/pypexel/issues)
[![Build Status](https://github.com/iwatkot/pypexel/actions/workflows/checks.yml/badge.svg)](https://github.com/iwatkot/pypexel/actions)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)<br>
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pypexel)](https://pypi.org/project/pypexel/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pypexel)](https://pypi.org/project/pypexel/)

</div>

## Overview
This SDK is designed to interact with the [Pexels API](https://www.pexels.com/api/) in a more object-oriented way. It provides asynchronous methods to interact with the API. The SDK is designed to be as simple as possible to use, while still providing a lot of flexibility and uses `Pydantic` models to validate the data.<br>
Used dependencies:
- `httpx` for asynchronous API
- `pydantic` for models

Supported Python versions:
- 3.11
- 3.12

## Quick Start
After installing the SDK, you can create a new instance of the API. When creating a new instance, you can either use environment variables or pass the credentials directly. It's strongly recommended to use environment variables to store the API credentials.<br>

### Installation
```bash
pip install pypexel
```

### Create a new instance of the API
It's recommended to use an environment variable to store the API credentials:
```python
import os

os.environ["PEXELS_API_KEY"] = "your-api-key"
```

To work asynchronously:
```python
import pypexel as pex

# Using environment variables:
api = pex.AsyncApi.from_env()

# Or using the credentials directly:
api = pex.AsyncApi("your-api-key")
```

## Examples
You'll find detailed docs with usage examples for both APIs and for used models in the corresponding package directories:
- [Asynchronous API](pypexel/async_api/README.md)
- [Models](pypexel/models/README.md)

In this section, you'll find some examples of how to use the SDK. You can also check out the [demo.py](demo.py) file in the root directory for more examples.

### Search for photos
```python
import asyncio
import os
import pypexel as pex

os.environ["PEXELS_API_KEY"] = "your-api-key"

api = pex.AsyncApi.from_env()

async def main():
    # Search for photos with the query "nature"
    photos = await api.photos.search("nature", limit=10)
    
    # Print the first photo's URL
    if photos:
        print(photos[0].src.original)
    else:
        print("No photos found.")

asyncio.run(main())
```

### Search for videos
```python
import asyncio
import os
import pypexel as pex

os.environ["PEXELS_API_KEY"] = "your-api-key"
api = pex.AsyncApi.from_env()

async def main():
    # Search for videos with the query "nature"
    videos = await api.videos.search("nature", limit=10)
    
    # Print the first video URL
    if videos:
        print(videos[0].video_files[0].link)
    else:
        print("No videos found.")

asyncio.run(main())
```

## Bugs and Feature Requests
If you find a bug or have a feature request, please open an issue on the GitHub repository.<br>
You're also welcome to contribute to the project by opening a pull request.
