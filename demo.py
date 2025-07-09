# 1️⃣ Create a virtual environment and install pypexel:
# ```bash
# python -m venv .venv
# source .venv/bin/activate  # For Linux/Mac
# .venv\Scripts\activate  # For Windows
# pip install pypexel

import asyncio
import os

# 2️⃣ Import the pypexel library.
import pypexel as pex

# 3️⃣ Create an instance of AsyncApi with your API token.
# Option 1: Set the API key directly.
api_token = "your_api_token_here"
api = pex.AsyncApi(token=api_token)

# Option 2: Set the API key as an environment variable.
os.environ["PEXELS_API_KEY"] = "your_api_token_here"
api = pex.AsyncApi.from_env()


async def main():
    # 4️⃣ Work with photos.
    photos: list[pex.Photo] = await api.photos.search("nature", limit=5)
    print(f"Found {len(photos)} photos.")

    for photo in photos:
        # 5️⃣ Use the .src property to get the actual download links for different sizes.
        download_link = photo.src.original
        print(
            f"Photo ID: {photo.id}, Photographer: {photo.photographer}, Download Link: {download_link}"
        )

    # 6️⃣ Work with videos.
    videos: list[pex.Video] = await api.videos.search("nature", limit=5)
    print(f"Found {len(videos)} videos.")

    for video in videos:
        # 7️⃣ Use the .video_files property to get the download links for different video qualities.
        download_link = video.video_files[0].link
        print(
            f"Video ID: {video.id}, Photographer: {video.photographer}, Download Link: {download_link}"
        )

    # 8️⃣ Work with collections.
    collections: list[pex.Collection] = await api.collections.search("nature", limit=5)
    print(f"Found {len(collections)} collections.")

    collection = collections[0]

    # 9️⃣ Get media from a collection.
    media: list[pex.Photo | pex.Video] = await api.collections.media(
        collection_id=collection.id,
    )
    for item in media:
        if isinstance(item, pex.Photo):
            print(f"Photo ID: {item.id}, Photographer: {item.photographer}")
        elif isinstance(item, pex.Video):
            print(f"Video ID: {item.id}, Duration: {item.duration} seconds")


if __name__ == "__main__":
    # 🔟 Run the script.
    asyncio.run(main())
# Note: Replace "your_api_token_here" with your actual Pexels API token.
# You can obtain an API token by signing up at https://www.pexels.com/api/.
