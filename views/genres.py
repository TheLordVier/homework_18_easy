
from flask import request
from flask_restx import Resource, Namespace
from setup_db import db
from models import Genre, GenreSchema

# Создаём неймcпейс для представлений
genre_ns = Namespace('genres')

# Cоздаём экземпляры схем
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

@genre_ns.route("/")
class GenresView(Resource):
# Получение списка всех сущностей
    def get(self):
        genres = db.session.query(Genre)
        return genres_schema.dump(genres), 200

# Создание определённой сущности
    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "Genre created", 201


# Регистрируем класс (CBV) по эндпоинту указанному в genre_ns
@genre_ns.route("/<int:gid>")
class GenreView(Resource):
# Получение конкретной сущности по идентификатору
    def get(self, gid: int):
        try:
            genre = db.session.query(Genre).get(gid)
            return genre_schema.dump(genre), 200
        except Exception:
            return str(Exception), 404

# Обновление конкретной сущности по идентификатору
    def put(self, gid: int):
        genre = db.session.query(Genre).get(gid)
        req_json = request.json
        if "name" in req_json:
            genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "Genre updated", 204

# Удаление конкретной сущности по идентификатору
    def delete(self, gid: int):
        genre = db.session.query(Genre).get(gid)
        if not genre:
            return "Genre not found", 400
        db.session.delete(genre)
        db.session.commit()
        return "Genre deleted", 204
