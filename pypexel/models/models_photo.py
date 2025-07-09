"""This module defines the data models for photos used in the Pypexel application."""

from pydantic import BaseModel


class PhotoSrc(BaseModel):
    """Data model for photo source URLs."""

    original: str
    large2x: str
    large: str
    medium: str
    small: str
    portrait: str
    landscape: str
    tiny: str


class Photo(BaseModel):
    """Data model for a photo."""

    id: int
    width: int
    height: int
    url: str
    photographer: str
    photographer_url: str
    photographer_id: int
    avg_color: str
    src: PhotoSrc
    liked: bool
    alt: str
