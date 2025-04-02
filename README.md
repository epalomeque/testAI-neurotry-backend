# ¿Por qué usar pgvector?
Permite almacenar embeddings y hacer búsquedas por similitud con cosine similarity o L2 distance.
- Escalabilidad: Se integra con bases de datos existentes y soporta índices optimizados para búsquedas rápidas.
- Persistencia: No perderemos datos ni embeddings al reiniciar el servidor.

## Correr postgresql con vector
`docker run --name pgvector-db -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=recommendations -d ankane/pgvector`

## Habilitar vector 
`CREATE EXTENSION IF NOT EXISTS vector;`

## Crear tabla en postgresql

`
CREATE TABLE peliculas (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    embedding VECTOR(384) -- Dimensión del modelo de embeddings
);
`

---

# Como probarlo

## Instalar dependencias
`pip install -r requirements.txt`

## Ejecutar el servidor
`python nombre_del_script.py`

## Agregar una pelicula
`POST http://127.0.0.1:8000/agregar_pelicula/?titulo=John Wick&descripcion=Un ex asesino busca venganza contra la mafia que mató a su perro.`

## Obtener recomendaciones
`GET http://127.0.0.1:8000/recomendar/?descripcion=Un hombre busca venganza después de perder a su familia`
