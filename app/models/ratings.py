from __future__ import annotations
from typing import Optional
from sqlalchemy import BigInteger, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Ratings(Base):
    __tablename__ = "ratings"

    # Composite key not explicitly declared as PK in DDL; SQLAlchemy needs a PK
    # We'll create a surrogate implicit composite key by marking both as primary keys
    userId: Mapped[int] = mapped_column(Integer, primary_key=True)
    movieId: Mapped[int] = mapped_column(Integer, primary_key=True)

    rating: Mapped[float] = mapped_column(Numeric(2, 1, asdecimal=False), nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False)


