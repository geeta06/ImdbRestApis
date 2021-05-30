'''This is model file for the projects '''
from . import db
import random


def generate_movie_id():
    """
    generates random 10 digit alphanumeric combination string
    :return: string
    """
    movie_id = "" + "".join(
        [random.choice('123456789ABCDEFGHIJKLMNPQRSTUVXYZ') for i in range(10)])
    return movie_id


class User(db.Model):
    """
    This model is used to create user based on type in this system
    currently there is only one user which is admin
    later on we can more if required
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    usertype = db.Column(db.String(50))
    password = db.Column(db.String(80))


#this is association table for movie and genre
movie_genre = db.Table('movie_genre',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')),
    db.Column('movies_id', db.Integer, db.ForeignKey('movies.id'))
    )


class Genre(db.Model):
    """
    Genre is a movie types each genre can be have many movies
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    movies = db.relationship('Movies', secondary=movie_genre,
            backref=db.backref('movie_genre_table_backref', lazy='dynamic'))

    def __repr__(self):
        return str(self.name)


class Movies(db.Model):
    """
    Movies is used to store description of movies a movie can have multiple genre
    """
    id = db.Column(db.Integer, primary_key=True)
    movies_id = db.Column(db.String(20), unique=True, default=generate_movie_id)
    name = db.Column(db.String(100), unique=True)
    director_name = db.Column(db.String(50))
    imdb_score = db.Column(db.Float)
    popularity = db.Column(db.Float)

    @property
    def serialize(self):
        """
        to get serialize data for movie model
        :return: dict
        """
        return {
            'movies_id': self.movies_id,
            'name': self.name,
            'director': self.director_name,
            'imdb_score': self.imdb_score,
            '99popularity': self.popularity,
            'genre': [str(i) for i in self.movie_genre_table_backref.all()]
        }





