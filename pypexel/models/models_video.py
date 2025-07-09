"""This module defines the data models for videos."""

from pydantic import BaseModel


class VideoFile(BaseModel):
    """Model representing a video file."""

    id: int
    quality: str
    file_type: str
    width: int | None = None
    height: int | None = None
    link: str


class VideoPicture(BaseModel):
    """Model representing a video picture."""

    id: int
    picture: str
    nr: int


class Video(BaseModel):
    """Model representing a video."""

    id: int
    width: int
    height: int
    url: str
    image: str
    duration: int
    user: dict[str, str | int]
    video_files: list[VideoFile]
    video_pictures: list[VideoPicture]
