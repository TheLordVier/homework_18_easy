
from flask import request
from flask_restx import Resource, Namespace
from setup_db import db
from models import Director, DirectorSchema

# Создаём неймcпейс для представлений
director_ns = Namespace('directors')

# Cоздаём экземпляры схем
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route("/")
class DirectorsView(Resource):
# Получение списка всех сущностей
    def get(self):
        directors = db.session.query(Director)
        return directors_schema.dump(directors), 200

# Создание определённой сущности
    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        db.session.add(new_director)
        return "Director created", 201


# Регистрируем класс (СBV) по эндпоинту указанному в director_ns
@director_ns.route("/<int:did>")
class DirectorView(Resource):
# Получение конкретной сущности по идентификатору
    def get(self, did: int):
        try:
            director = db.session.query(Director).get(did)
            return director_schema.dump(director), 200
        except Exception:
            return str(Exception), 404

# Обновление конкретной сущности по идентификатору
    def put(self, did: int):
        req_json = request.json
        director = db.session.query(Director).get(did)
        if "name" in req_json:
            director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "Director updated", 204

# Удаление конкретной сущности по идентификатору
    def delete(self, did: int):
        director = db.session.query(Director).get(did)
        if not director:
            return "Director not found", 400
        db.session.delete(director)
        db.session.commit()
        return "Director deleted", 204
