'''This file is used to write db operation related to movies models'''

#import starts from here...
from api import db
from api.models import Movies, Genre
from api.utils.helpers import remove_movie_genre



class MovieOperation():
    """
    this class is used to perform Movies Model related CRUD operations
    """

    @staticmethod
    def add_movie(name, director, imdb_score, popularity, genres):
        """
        This func is used for adding new entries of movie in db
        :param name: str movie name
        :param director: str director name
        :param imdb_score: float imdb score
        :param popularity: float in range 0-100
        :param genres: list of genres
        :return: movie object, flag
        """
        try:
            name = name.strip()
            director = director.strip()
            movie_exists = Movies.query.filter_by(name=name).first()
            if movie_exists:
                return movie_exists, False
            new_movie = Movies(
                name=name,
                director_name=director,
                imdb_score=imdb_score,
                popularity=popularity
            )
            db.session.add(new_movie)
            genrelist = [genre.strip(' ') for genre in genres]
            for genre in genrelist:
                response = Genre.query.filter_by(name=genre.upper()).first()
                if not response:
                    response = Genre(name=genre.upper())
                    db.session.add(response)
                new_movie.movie_genre_table_backref.append(response)
            db.session.commit()
            return new_movie, True
        except Exception as e:
            return None, False

    @staticmethod
    def update_movie(movies_id, name, director, imdb_score, popularity, genres):
        """
        This func is used to perform edit operation movie model
        :param movie_object: movie object which need to be modify
        :param name: str movie name
        :param director: str director name
        :param imdb_score: float score in range 0-10
        :param popularity: float popularity in range 0-100
        :param genres: list of genres
        :return: movie object , flag
        """
        try:
            movie_object = Movies.query.filter_by(movies_id=movies_id).first()
            if not movie_object:
                return "Movie doesn't exists", False
            name = name.strip()
            director = director.strip()
            movie_object.name = name
            movie_object.director_name = director
            movie_object.imdb_score = imdb_score
            movie_object.popularity = popularity
            genrelist = [genre.strip(' ') for genre in genres]
            remove_movie_genre(movie_object)
            for genre in genrelist:
                response = Genre.query.filter_by(name=genre.upper()).first()
                if not response:
                    response = Genre(name=genre.upper())
                    db.session.add(response)
                movie_object.movie_genre_table_backref.append(response)
            db.session.commit()
            return movie_object, True
        except Exception as e:
            return None, False

    @staticmethod
    def delete_movie(movies_id):
        """
        this func is used to delete a movie entry based on its name
        :param name: str name of the existing movie
        :return: message, flag
        """
        try:
            movie = Movies.query.filter_by(movies_id=movies_id).first()
            if not movie:
                response = "Movie with given id not found"
                return response, False

            db.session.delete(movie)
            db.session.commit()
            return movie, True

        except Exception as e:
            return None, False


    @staticmethod
    def get_movies_list(offset, limit):
        movies = Movies.query.all()
        return [movie.serialize for movie in list(movies)[offset:limit]]


    @staticmethod
    def get_search_result(name, director, imdb_score, popularity, genre, limit, offset):
        """
        this func is used to perform search movie based on any parameter of movie models
        like name or director or imdb score or genre or popularity
        :param name: str movie name
        :param director: str director name
        :param imdb_score: float imdb score in range 1-10
        :param popularity: float popularity in range 1-100
        :param genre: str genre type
        :param limit: int default 10
        :param offset: int default 0
        :return: list of movies objects based on search
        """
        try:
            responseResult = []
            if name:
                name = ''.join(('%', name, '%'))
                responseResult = Movies.query.filter(Movies.name.ilike(name))

            if director:
                director = ''.join(('%', director, '%'))
                responseResult = Movies.query.filter(Movies.director_name.ilike(director))

            if imdb_score:
                responseResult = Movies.query.filter(Movies.imdb_score >= imdb_score)

            if popularity:
                responseResult = Movies.query.filter(Movies.popularity >= popularity)

            if genre:
                genre_object = Genre.query.filter(Genre.name.ilike(genre)).first()
                if genre_object:
                    responseResult = [i for i in genre_object.movies]
                    return responseResult[offset: limit]

            return list(responseResult)[offset: limit]
        except Exception as e:
            return []

