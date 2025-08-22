from __future__ import annotations
from typing import Optional
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Keywords(Base):
    __tablename__ = "keywords"

    # No primary key in DDL; add surrogate composite key for ORM identity
    movieId: Mapped[int] = mapped_column(Integer, primary_key=True)
    keyword: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)


