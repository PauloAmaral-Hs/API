from sqlalchemy import text
from app.db.session import engine

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()
            print(f"✅ Conexão com PostgreSQL bem-sucedida!")
            print(f"Versão: {version[0]}")
            
            # Testar se as tabelas existem
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result.fetchall()]
            print(f"📋 Tabelas encontradas: {tables}")
            
            # Contar registros em cada tabela
            for table in tables:
                result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.fetchone()[0]
                print(f"   {table}: {count} registros")
                
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")

if __name__ == "__main__":
    test_connection()
