from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from db.session import get_db  # Mudança: era "app.db.session"
from routers import movies, ai  # Mudança: era "app.routers"
from core.config import settings  # Mudança: era "app.core.config"

app = FastAPI(
    title=settings.APP_NAME,
    description="API de filmes com integração de IA para consultas inteligentes",
    version="1.0.0"
)

# Include routers
app.include_router(movies.router, prefix="/api/v1", tags=["movies"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API de Filmes com IA!",
        "docs": "/docs",
        "endpoints": {
            "movies": "/api/v1/movies",
            "ai_query": "/api/v1/ai/query"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)