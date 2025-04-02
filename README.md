# Backend: Recomendador de Películas con FastAPI y PostgreSQL
El backend de este sistema es una API desarrollada con FastAPI, diseñada para recomendar películas basadas en una descripción ingresada por el usuario. Utiliza inteligencia artificial y búsqueda semántica para encontrar películas similares en función del contenido proporcionado.
## Funcionalidad Principal
1. Almacenamiento de Películas en PostgreSQL
   - Se utiliza PostgreSQL como base de datos principal.
   - Los títulos y descripciones de las películas se almacenan junto con sus embeddings semánticos, generados mediante el modelo de inteligencia artificial Sentence Transformers.
   - Se usa la extensión pgvector en PostgreSQL para realizar búsquedas eficientes basadas en similitud semántica.
2. Procesamiento del Lenguaje Natural con Sentence Transformers
   - Cada película tiene un vector de embedding que representa su significado en un espacio multidimensional.
   - Cuando un usuario ingresa una descripción, la API convierte ese texto en un embedding y busca en la base de datos las películas más similares.
3. Endpoints del Backend
   - `POST /agregar_pelicula/ → Agrega una nueva película con su título y descripción a la base de datos.`
   - `GET /recomendar/ → Recibe una descripción y devuelve las películas más similares.`
## Tecnologías Utilizadas
- FastAPI → Framework rápido para construir APIs en Python.
- Sentence Transformers → Modelo de IA para entender el significado de textos.
- PostgreSQL + pgvector → Base de datos optimizada para búsqueda semántica.
- SQLAlchemy → Para gestionar la conexión con la base de datos.
---
## Instalación

### Correr postgresql con vector
`docker run --name pgvector-db -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=recommendations -d ankane/pgvector`

### Habilitar vector 
`CREATE EXTENSION IF NOT EXISTS vector;`

### Crear tabla en postgresql

`
CREATE TABLE peliculas (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    embedding VECTOR(384) -- Dimensión del modelo de embeddings
);
`

---

## Como probarlo

### Instalar dependencias
`pip install -r requirements.txt`

### Ejecutar el servidor
`python main.py`

### Agregar una pelicula
`POST http://127.0.0.1:8000/agregar_pelicula/?titulo=John Wick&descripcion=Un ex asesino busca venganza contra la mafia que mató a su perro.`

### Obtener recomendaciones
`GET http://127.0.0.1:8000/recomendar/?descripcion=Un hombre busca venganza después de perder a su familia`
