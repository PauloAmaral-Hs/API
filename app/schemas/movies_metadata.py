from __future__ import annotations
from datetime import date
from typing import Any, Optional
from pydantic import BaseModel
try:  # Pydantic v2
    from pydantic import ConfigDict  # type: ignore
except Exception:  # Pydantic v1 fallback
    ConfigDict = None  # type: ignore


class MoviesMetadata(BaseModel):
    id: int

    adult: Optional[bool] = None
    belongs_to_collection: Optional[Any] = None
    budget: Optional[int] = None
    genres: Optional[Any] = None
    homepage: Optional[str] = None
    imdb_id: Optional[str] = None
    original_language: Optional[str] = None
    original_title: Optional[str] = None
    overview: Optional[str] = None
    popularity: Optional[float] = None
    poster_path: Optional[str] = None
    production_companies: Optional[Any] = None
    production_countries: Optional[Any] = None
    release_date: Optional[date] = None
    revenue: Optional[int] = None
    runtime: Optional[float] = None
    spoken_languages: Optional[Any] = None
    status: Optional[str] = None
    tagline: Optional[str] = None
    title: Optional[str] = None
    video: Optional[bool] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None

    # Pydantic v2 config (ignored by v1). v1 uses inner Config below
    model_config = ConfigDict(from_attributes=True) if ConfigDict else None  # type: ignore

    class Config:  # Pydantic v1 compatibility
        orm_mode = True


