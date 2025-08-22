from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
import openai
from typing import List, Dict, Any
import json
from db.session import get_db  # Mudança: era "app.db.session"
from core.config import settings  # Mudança: era "app.core.config"
from models.movies_metadata import MoviesMetadata  # Mudança
from models.credits import Credits  # Mudança

# ... resto do código permanece igual ...

router = APIRouter()

# Configurar OpenAI
if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY

class MovieAI:
    def __init__(self, db: Session):
        self.db = db
    
    def get_movie_context(self, query: str) -> str:
        """Extrair contexto relevante da base de dados para a consulta"""
        # Buscar filmes relacionados à consulta
        movies = self.db.query(MoviesMetadata).filter(
            or_(
                MoviesMetadata.title.ilike(f"%{query}%"),
                MoviesMetadata.overview.ilike(f"%{query}%"),
                MoviesMetadata.genres.contains([{"name": query}])
            )
        ).limit(10).all()
        
        context = "Base de dados de filmes disponível:\n\n"
        for movie in movies:
            context += f"Título: {movie.title}\n"
            context += f"Ano: {movie.release_date.year if movie.release_date else 'N/A'}\n"
            context += f"Gênero: {movie.genres}\n"
            context += f"Sinopse: {movie.overview[:200]}...\n"
            context += f"Avaliação: {movie.vote_average}/10\n"
            context += f"Receita: ${movie.revenue:,}\n\n"
        
        return context
    
    def query_ai(self, user_question: str, context: str) -> str:
        """Consultar OpenAI com contexto da base de dados"""
        if not settings.OPENAI_API_KEY:
            return "API da OpenAI não configurada. Configure OPENAI_API_KEY no arquivo .env"
        
        try:
            prompt = f"""
            Você é um assistente especializado em filmes. Use a seguinte base de dados para responder à pergunta do usuário.
            
            {context}
            
            Pergunta do usuário: {user_question}
            
            Responda de forma clara e útil, baseando-se nos dados disponíveis. Se não houver informações suficientes, indique isso.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em filmes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erro ao consultar IA: {str(e)}"

@router.post("/query")
async def ai_query(
    question: str = Query(..., description="Sua pergunta sobre filmes"),
    db: Session = Depends(get_db)
):
    """Consultar IA sobre filmes usando a base de dados"""
    ai = MovieAI(db)
    
    # Extrair contexto relevante
    context = ai.get_movie_context(question)
    
    # Consultar IA
    response = ai.query_ai(question, context)
    
    return {
        "question": question,
        "response": response,
        "context_used": context[:500] + "..." if len(context) > 500 else context
    }

@router.get("/recommendations")
async def get_ai_recommendations(
    user_preferences: str = Query(..., description="Descreva seus gostos em filmes"),
    db: Session = Depends(get_db)
):
    """Obter recomendações de filmes usando IA"""
    ai = MovieAI(db)
    
    # Buscar filmes populares para contexto
    popular_movies = db.query(MoviesMetadata).filter(
        MoviesMetadata.vote_average >= 7.0,
        MoviesMetadata.vote_count >= 100
    ).order_by(MoviesMetadata.popularity.desc()).limit(20).all()
    
    context = "Filmes populares disponíveis:\n\n"
    for movie in popular_movies:
        context += f"Título: {movie.title}\n"
        context += f"Gênero: {movie.genres}\n"
        context += f"Avaliação: {movie.vote_average}/10\n\n"
    
    # Consultar IA para recomendações
    question = f"Baseado nestes filmes populares, recomende filmes para alguém que gosta de: {user_preferences}"
    response = ai.query_ai(question, context)
    
    return {
        "user_preferences": user_preferences,
        "recommendations": response,
        "popular_movies_analyzed": len(popular_movies)
    }

@router.get("/analysis")
async def analyze_movies_ai(
    analysis_type: str = Query(..., description="Tipo de análise (trends, patterns, insights)"),
    db: Session = Depends(get_db)
):
    """Análise de filmes usando IA"""
    ai = MovieAI(db)
    
    # Buscar dados para análise
    movies = db.query(MoviesMetadata).filter(
        MoviesMetadata.release_date.isnot(None),
        MoviesMetadata.vote_average.isnot(None)
    ).order_by(MoviesMetadata.release_date.desc()).limit(100).all()
    
    context = "Dados de filmes para análise:\n\n"
    for movie in movies:
        context += f"Título: {movie.title}, Ano: {movie.release_date.year}, Avaliação: {movie.vote_average}, Gênero: {movie.genres}\n"
    
    question = f"Analise estes dados de filmes e forneça insights sobre: {analysis_type}"
    response = ai.query_ai(question, context)
    
    return {
        "analysis_type": analysis_type,
        "insights": response,
        "movies_analyzed": len(movies)
    }
