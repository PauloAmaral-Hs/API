from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
try:  # Pydantic v2
    from pydantic import ConfigDict  # type: ignore
except Exception:  # Pydantic v1 fallback
    ConfigDict = None  # type: ignore


class Links(BaseModel):
    movieId: int
    imdbId: Optional[int] = None
    tmdbId: Optional[int] = None

    model_config = ConfigDict(from_attributes=True) if ConfigDict else None  # type: ignore

    class Config:
        orm_mode = True


