from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text
import numpy as np

# Configuración de PostgreSQL
DB_USER = 'user'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/recommendations"
engine = create_engine(DB_URL)

# Inicializar FastAPI
app = FastAPI()

# Cargar modelo de embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Función para recomendar películas
def recomendar_peliculas(descripcion_usuario, top_n=5):
    embedding_usuario = model.encode([descripcion_usuario])[0]  # Generar embedding

    with engine.connect() as conn:
        query = text("""
            SELECT titulo, descripcion, 1 - (embedding <=> :embedding) AS similitud
            FROM peliculas
            ORDER BY similitud DESC
            LIMIT :top_n
        """)
        result = conn.execute(query, {"embedding": embedding_usuario.tolist(), "top_n": top_n}).fetchall()

    return [{"titulo": row[0], "descripcion": row[1], "similitud": row[2]} for row in result]


# Endpoint para obtener recomendaciones de películas
@app.get("/recomendar/")
def obtener_recomendaciones(descripcion: str, top_n: int = 5):
    recomendaciones = recomendar_peliculas(descripcion, top_n)
    return {"descripcion_usuario": descripcion, "recomendaciones": recomendaciones}


# Endpoint para agregar nuevas películas
@app.post("/agregar_pelicula/")
def agregar_pelicula(titulo: str, descripcion: str):
    embedding = model.encode([descripcion])[0]  # Generar embedding

    with engine.connect() as conn:
        query = text(
            "INSERT INTO peliculas (titulo, descripcion, embedding) VALUES (:titulo, :descripcion, :embedding)")
        conn.execute(query, {"titulo": titulo, "descripcion": descripcion, "embedding": embedding.tolist()})
        conn.commit()

    return {"mensaje": f"Película '{titulo}' agregada exitosamente"}


# Ejecutar la API
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
