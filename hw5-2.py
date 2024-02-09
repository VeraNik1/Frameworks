import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import json

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Home work 5 task 2"}


class Movie(BaseModel):
    id: int
    title: str
    description: str
    genre: str

with open('movies.json', 'r', encoding='utf-8') as fh:
    movies = json.load(fh)

@app.get("/movie/", response_model=list[Movie])
async def show_movies():
    logger.info('Отработал GET-запрос показать списки фильмов.')
    return movies


@app.get("/movie/{movie_genre}/")
async def show_movies_by_genre(movie_genre: str):
    research = []
    for movie in movies:
        if movie['genre'] == movie_genre:
            research.append(movie)
            logger.info(f'Отработал GET-запрос на получение фильмов по жанру: {movie_genre}')
    if research:
        return research
    return HTTPException(status_code=404, detail="Movie not found")



@app.post("/movie/", response_model=Movie)
async def append_movie(movie: Movie):
    movies.append(movie)
    logger.info('Отработал POST-запрос на добавление фильма.')
    return movie


@app.put("/movie/{movie_id}/")
async def update_movie(movie_id: int, movie: Movie):
    for i, movie_ in enumerate(movies):
        if movie_['id'] == movie_id:
            movies[i] = movie
            logger.info(f'Отработал PUT-запрос для фильма: {movie_id}')
            return movie
    return HTTPException(status_code=404, detail="Movie not found")


@app.delete("/movie/{movie_id}/")
async def delete_movie(movie_id):
    for movie in movies:
        if movie['id'] == int(movie_id):
            movies.remove(movie)
            logger.info(f'Отработал DELETE-запрос для фильма: {movie_id}')
            return movies
    return HTTPException(status_code=404, detail="Movie not found")

if __name__ == '__main__':
    uvicorn.run('hw5-2:app', host='127.0.0.1', port=8000, reload=True)