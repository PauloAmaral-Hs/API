from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, text
from typing import List, Optional
import json
from db.session import get_db  # Mudança: era "app.db.session"
from models.movies_metadata import MoviesMetadata  # Mudança: era "app.models.movies_metadata"
from models.credits import Credits  # Mudança: era "app.models.credits"
from schemas.movies_metadata import MoviesMetadata as MoviesMetadataSchema  # Mudança
from schemas.credits import Credits as CreditsSchema  # Mudança

# ... resto do código permanece igual ...
router = APIRouter()

@router.get("/movies", response_model=List[MoviesMetadataSchema])
async def get_movies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    title: Optional[str] = None,
    genre: Optional[str] = None,
    year: Optional[int] = None,
    min_rating: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Buscar filmes com filtros opcionais"""
    query = db.query(MoviesMetadata)
    
    if title:
        query = query.filter(
            or_(
                MoviesMetadata.title.ilike(f"%{title}%"),
                MoviesMetadata.original_title.ilike(f"%{title}%")
            )
        )
    
    if genre:
        query = query.filter(MoviesMetadata.genres.contains([{"name": genre}]))
    
    if year:
        query = query.filter(MoviesMetadata.release_date >= f"{year}-01-01")
        query = query.filter(MoviesMetadata.release_date <= f"{year}-12-31")
    
    if min_rating:
        query = query.filter(MoviesMetadata.vote_average >= min_rating)
    
    movies = query.offset(skip).limit(limit).all()
    return movies

@router.get("/movies/{movie_id}", response_model=MoviesMetadataSchema)
async def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Buscar filme por ID"""
    movie = db.query(MoviesMetadata).filter(MoviesMetadata.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return movie

@router.get("/movies/{movie_id}/credits", response_model=CreditsSchema)
async def get_movie_credits(movie_id: int, db: Session = Depends(get_db)):
    """Buscar créditos de um filme"""
    credits = db.query(Credits).filter(Credits.movie_id == movie_id).first()
    if not credits:
        raise HTTPException(status_code=404, detail="Créditos não encontrados")
    return credits

@router.get("/movies/search/advanced")
async def advanced_search(
    query: str = Query(..., description="Texto para busca"),
    min_budget: Optional[int] = None,
    max_budget: Optional[int] = None,
    language: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Busca avançada em filmes"""
    search_query = db.query(MoviesMetadata)
    
    # Busca por texto em título, sinopse e tagline
    search_query = search_query.filter(
        or_(
            MoviesMetadata.title.ilike(f"%{query}%"),
            MoviesMetadata.overview.ilike(f"%{query}%"),
            MoviesMetadata.tagline.ilike(f"%{query}%")
        )
    )
    
    if min_budget:
        search_query = search_query.filter(MoviesMetadata.budget >= min_budget)
    
    if max_budget:
        search_query = search_query.filter(MoviesMetadata.budget <= max_budget)
    
    if language:
        search_query = search_query.filter(MoviesMetadata.original_language == language)
    
    movies = search_query.limit(50).all()
    return {"results": movies, "total": len(movies)}

@router.get("/genres/stats")
async def get_genre_statistics(db: Session = Depends(get_db)):
    """Estatísticas por gênero"""
    # Esta é uma implementação simplificada
    # Em produção, você pode usar queries SQL mais complexas
    movies = db.query(MoviesMetadata).all()
    
    genre_stats = {}
    for movie in movies:
        if movie.genres:
            for genre in movie.genres:
                genre_name = genre.get("name", "Unknown")
                if genre_name not in genre_stats:
                    genre_stats[genre_name] = {
                        "count": 0,
                        "avg_rating": 0,
                        "total_revenue": 0
                    }
                
                genre_stats[genre_name]["count"] += 1
                if movie.vote_average:
                    genre_stats[genre_name]["avg_rating"] += movie.vote_average
                if movie.revenue:
                    genre_stats[genre_name]["total_revenue"] += movie.revenue
    
    # Calcular médias
    for genre in genre_stats:
        if genre_stats[genre]["count"] > 0:
            genre_stats[genre]["avg_rating"] /= genre_stats[genre]["count"]
    
    return genre_stats
