# здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки). сюда импортируются сервисы из пакета service

from flask import request
from flask_restx import Resource, Namespace
from setup_db import db
from models import MovieSchema, Movie

# Создаём неймcпейс для представлений
movie_ns = Namespace('movies')

# Cоздаём экземпляры схем
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies = db.session.query(Movie)
        director_id = request.args.get("director_id")
        if director_id is not None:
            movies = movies.filter(Movie.director_id == director_id)
        genre_id = request.args.get("genre_id")
        if genre_id is not None:
            movies = movies.filter(Movie.genre_id == genre_id)
        year = request.args.get("year")
        if year is not None:
            movies = movies.filter(Movie.year == year)
        return movies_schema.dump(movies.all()), 200

    def post(self):
        """"
        Создание определённой сущности (фильма)
        """
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "Movie created", 201


    # def post(self):
    #     req_json = request.json
    #     ent = Movie()
    #
    #     db.session.add(ent)
    #     db.session.commit()
    #     return "", 201, {"location": f"/movies/{ent.id}"}

@movie_ns.route("/<int:mid>")
class MovieView(Resource):
    def get(self, mid: int):
        try:
            movie = db.session.query(Movie).get(mid)
            return movie_schema.dump(movie), 200

        except Exception as e:
            return str(e), 404

    def put(self, mid: int):
        movie = db.session.query(Movie).get(mid)
        req_json = request.json

        movie.title = req_json.get('title')
        movie.description = req_json.get('description')
        movie.trailer = req_json.get('trailer')
        movie.year = req_json.get('year')
        movie.rating = req_json.get('rating')
        movie.genre_id = req_json.get('genre_id')
        movie.director_id = req_json.get('director_id')

        db.session.add(movie)
        db.session.commit()
        return 'Movie updated', 204

    def delete(self, mid: int):
        movie = db.session.query(Movie).get(mid)
        if not movie:
            return "Movie not found", 400
        db.session.delete(movie)
        db.session.commit()
        return "Movie deleted", 204
