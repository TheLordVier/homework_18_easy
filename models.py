# здесь модель SQLAlchemy для сущности, также могут быть дополнительные методы работы с моделью (но не с базой)

# чтобы создать БД с данными
from setup_db import db
# Импортируем библиотеку Marshmallow
from marshmallow import Schema, fields


# Создаём модель Movie с соответствуюшими сущностями
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.String(250))
    trailer = db.Column(db.String(250))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


# Описываем модель Movie в виде класса схемы
class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    # genre_id = fields.Int()
    # director_id = fields.Int()


# Создаём модель Director с соответствуюшими сущностями
class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))


# Описываем модель Director в виде класса схемы
class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


# Создаём модель Genre с соответствуюшими сущностями
class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


# Описываем модель Genre в виде класса схемы
class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
