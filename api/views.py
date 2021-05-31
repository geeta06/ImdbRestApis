'''This file used to write endpoints of api '''
from flask import Blueprint, jsonify
from flask import request, make_response


import logging
from logging.config import dictConfig

from api.entity.movies import MovieOperation
from api.config.settings import Config
from api.utils.jwt import admin_jwt_token_required
from api.utils.validators import Validators, InputOutOfBounds
from api.utils.helpers import required_field_difference
from api.utils.statusCodes import StatusCode


main = Blueprint('main', __name__)

dictConfig(Config.LOG_CONFIGURATION)
logger = logging.getLogger(__name__)

limit = 10


@main.route('/')
def homepage():
    """
    A test API to check if flask is properly configured
    :return:
    """
    return "Hello Humans"


@main.route('/api/v1/movies', methods=["GET"])
def get_movies():
    """
    GET api used by any users who wants to get list of movies
    :return JsonResponse
    [{
      "99popularity": 83.0,
      "director": "Victor Fleming",
      "genre": [
        "ADVENTURE",
        "FAMILY",
        "FANTASY",
        "MUSICAL"
      ],
      "imdb_score": 8.3,
      "name": "The Wizard of Oz"
    },
    {
      "99popularity": 88.0,
      "director": "George Lucas",
      "genre": [
        "ACTION",
        "ADVENTURE",
        "FANTASY",
        "SCI-FI"
      ],
      "imdb_score": 8.8,
      "name": "Star Wars"
        }
    ] 200 - OK
    500 - InternalServerError
    """
    try:
        offset = int(request.args.get('offset', 0))
        max_limit = offset + limit
        response = MovieOperation.get_movies_list(offset, max_limit)
        return make_response(jsonify(response), StatusCode._200)

    except Exception as e:
        logger.error("{} in get movie list".format(e))
        return make_response(jsonify({'message': str(e)}), StatusCode._500)


@main.route('/api/v1/search/movie', methods=["GET"])
def search_movie():
    """
    GET api is used by any user to search a movie based on rating, movie name,
    director name, imdb score or popularity
    :return:JsonResponse
    200- Ok
    400- No movie found
    500- InternalServerError
    """
    try:
        data = request.args
        offset = int(data.get('offset', 0))
        name = data.get('name', '')
        popularity = float(data.get('99popularity', 0.0))
        imdb_score = float(data.get('imdb_score', 0.0))
        director = data.get('director', '')
        genre = data.get('genre', '')
        max_limit = offset + limit
        movies = MovieOperation.get_search_result(
            name, director,
            imdb_score, popularity,
            genre, max_limit, offset)
        if movies == []:
            return make_response(jsonify("No movie found"), StatusCode._400)
        response = [movie.serialize for movie in movies]
        return make_response(jsonify(response), StatusCode._200)
    except Exception as e:
        logger.error("{} while searching movie".format(str(e)))
        return make_response(jsonify({'message': str(e)}), StatusCode._500)


@main.route('/api/v1/add/movie', methods=["POST"])
@admin_jwt_token_required
def add_movie():
    """
    POST api used by admin to add new movies in db
    headers = {"Content-Type": "application/json",
        "x-access-token" : "token-value"
     }
    required raw data format:
        {
        "99popularity": 66.0,
        "director": "Giovanni Pastrone",
        "genre": [
          "Adventure",
          " Drama",
          " War"
        ],
        "imdb_score": 6.6,
        "name": "Cabiria"
    }
    :return: JsonResponse
    {'message': "Movie Added Successfully." }  200 - OK
    {'message': response } 400 - Bad request
    {'message': response }, 500 ]- Internal Server Error
    """
    try:
        data = request.get_json()
        required_fields = [
                    'name',
                    'director',
                    'imdb_score',
                    '99popularity',
                    'genre'
                ]
        optional_fields = []
        # convert unicode to normal string
        post_params_key = map(str, data.keys())
        required, not_needed = required_field_difference(
                        required_fields,
                        optional_fields,
                        post_params_key
                    )

        # if extra fields is provided
        if not_needed:
            extra_field_response = Validators.extra_fields_response(not_needed)
            return make_response(jsonify({'message': extra_field_response}), StatusCode._400)

        # if required field not provided
        if required:
            field_missing = Validators.missing_fields_response(required)
            return make_response(jsonify({'message': field_missing}), StatusCode._400)

        name = data['name']
        director_name = data['director']
        imdb_score = data['imdb_score']
        popularity = data['99popularity']
        genres = data['genre']
        Validators.param_validation(popularity, imdb_score)

        response, status = MovieOperation.add_movie(
                        name,
                        director_name,
                        imdb_score,
                        popularity,
                        genres
                    )
        if status:
            logger.info("Movie Record Added Successfully")
            return make_response(
                jsonify({'message': 'Movie Added Successfully.'}), StatusCode._200)
        elif not status:
            return make_response(
                jsonify({'message': 'Movie Already Exists.'}), StatusCode._200)

    except InputOutOfBounds:
        return make_response(
            jsonify({'message': 'popularity or imdb score Out of Bound'}), StatusCode._400)

    except Exception as e:
        logger.error("{} while adding movie".format(str(data)))
        return make_response(jsonify({'message': str(e)}), StatusCode._500)


@main.route('/api/v1/update/movie', methods=["PUT"])
@admin_jwt_token_required
def update_movie():
    """
    Update Api for Admin to edit details
    of any existing movie in db.

    :return: JsonResponse
    """
    try:
        data = request.get_json()
        required_fields = [
            'movies_id',
            'name',
            'director',
            'imdb_score',
            '99popularity',
            'genre'
        ]
        optional_fields = []
        # convert unicode to normal string
        post_params_key = map(str, data.keys())
        required, not_needed = required_field_difference(
            required_fields,
            optional_fields,
            post_params_key
        )
        # if extra fields is provided
        if not_needed:
            extra_field_response = Validators.extra_fields_response(not_needed)
            return make_response(jsonify({'message': extra_field_response}), StatusCode._400)

        # if required field not provided
        if required:
            field_missing = Validators.missing_fields_response(required)
            return make_response(jsonify({'message': field_missing}), StatusCode._400)

        movies_id = data['movies_id']
        name = data['name']
        director = data['director']
        imdb_score = data['imdb_score']
        popularity = data['99popularity']
        genres = data['genre']

        Validators.param_validation(popularity, imdb_score)

        response, status = MovieOperation.update_movie(
            movies_id,
            name, director,
            imdb_score, popularity,
            genres)
        if status:
            logger.info("Movie Record Updated Successfully")
            return make_response(
                jsonify({'message': 'Movie Updated Successfully.'}), StatusCode._200)

        elif not status:
            return make_response(
                jsonify({'message': 'Movie  Exists.'}), StatusCode._200)
    except InputOutOfBounds:
        return make_response(
            jsonify({'message': 'popularity or imdb score Out of Bound'}), StatusCode._400)

    except Exception as e:
        logger.error("{} while updating movie id {}".format(str(e), movies_id))
        return make_response(jsonify({'message': str(e)}), StatusCode._500)


@main.route('/api/v1/delete/movie', methods=["DELETE"])
@admin_jwt_token_required
def delete_movie():
    """
    Delete Api for admin to delete movie by its name
    :return:JsonResponse

    200- Ok
    [{
    "message": "Movie Deleted Successfully."
    }, 200]
    400- Bad Request
    500- InternalServerError
    """
    try:
        data = request.get_json()
        movies_id = data['movies_id']
        if not movies_id:
            field_missing = Validators.missing_fields_response(['movies_id'])
            return make_response(jsonify({'message': field_missing}), StatusCode._400)
        response, status = MovieOperation.delete_movie(movies_id)
        if status:
            logger.info("Movie Record Deleted Successfully")
            return make_response(jsonify({'message': 'Movie Deleted Successfully.'}), StatusCode._200)

        return make_response(jsonify({'message': 'Movie Does not exists.'}), StatusCode._200)
    except Exception as e:
        logger.error("{} while deleting movie id {}".format(str(e), movies_id))
        return make_response(jsonify({'message': str(e)}), StatusCode._500)

