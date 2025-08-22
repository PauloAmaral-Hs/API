from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

try:  # Pydantic v2
    from pydantic import ConfigDict  # type: ignore
except Exception:  # Pydantic v1 fallback
    ConfigDict = None  # type: ignore


class Ratings(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int

    model_config = ConfigDict(from_attributes=True) if ConfigDict else None  # type: ignore

    class Config:  # v1
        orm_mode = True


