from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.session import Base  # Mudança aqui: era "app.db.session"
if TYPE_CHECKING:  # for type checkers only (avoids runtime circular import)
    from models.movies_metadata import MoviesMetadata  # Mudança aqui: era "app.models.movies_metadata"

# ... resto do código permanece igual ...

class Credits(Base):
    __tablename__ = "credits"

    movie_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("movies_metadata.id", ondelete="CASCADE", name="fk_credits_movie"),
        primary_key=True,
    )
    cast: Mapped[Optional[dict]] = mapped_column("cast", JSONB, nullable=True)
    crew: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    movie: Mapped["MoviesMetadata"] = relationship(
        "MoviesMetadata",
        back_populates="credits",
        uselist=False,
    )


