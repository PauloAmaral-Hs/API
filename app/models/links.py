from __future__ import annotations
from typing import Optional
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Links(Base):
    __tablename__ = "links"

    movieId: Mapped[int] = mapped_column(Integer, primary_key=True)
    imdbId: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tmdbId: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


