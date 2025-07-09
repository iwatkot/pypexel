"""This module defines the data models for collections used in the Pypexel application."""

from pydantic import BaseModel


class Collection(BaseModel):
    """Model representing a collection of media items."""

    id: str
    title: str
    description: str | None
    private: bool
    media_count: int
    photos_count: int
    videos_count: int
