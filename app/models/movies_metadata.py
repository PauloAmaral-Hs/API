from __future__ import annotations
from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import BigInteger, Boolean, Date, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.session import Base  # Mudança aqui: era "app.db.session"
if TYPE_CHECKING:  # for type checkers only (avoids runtime circular import)
    from models.credits import Credits  # Mudança aqui: era "app.models.credits"

# ... resto do código permanece igual ...


class MoviesMetadata(Base):
    __tablename__ = "movies_metadata"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Columns
    adult: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    belongs_to_collection: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    budget: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    genres: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    homepage: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    imdb_id: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    original_language: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    original_title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    overview: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    popularity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    poster_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    production_companies: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    production_countries: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    release_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    revenue: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    runtime: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    spoken_languages: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tagline: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    video: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    vote_average: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    vote_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationships
    credits: Mapped[Optional["Credits"]] = relationship(
        back_populates="movie",
        uselist=False,
        cascade="all, delete-orphan",
    )


