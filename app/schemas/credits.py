from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel
try:  # Pydantic v2
    from pydantic import ConfigDict  # type: ignore
except Exception:  # Pydantic v1 fallback
    ConfigDict = None  # type: ignore


class Credits(BaseModel):
    movie_id: int
    cast: Optional[Any] = None
    crew: Optional[Any] = None

    model_config = ConfigDict(from_attributes=True) if ConfigDict else None  # type: ignore

    class Config:
        orm_mode = True


