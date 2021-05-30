''' This File is use for writing generic functions '''

#import starts from here...
from api import db


#functions start from here...
def remove_movie_genre(movie_object):
    """
    this function is used for removing entry from associate table
    of movie_genre
    :param movie_object: movie object
    :return: None
    """
    for movie in movie_object.movie_genre_table_backref.all():
        movie_object.movie_genre_table_backref.remove(movie)
        db.session.commit()


def required_field_difference(required_field, optional_fields, parameters):
    """
    compare three list and returns the required field and not_needed fields
    :param required_field: the list of fields which required
    :param optional_fields: the list of fields which are optional
    :param parameters:
    :return: list
    """
    required_field_set = set(required_field)
    optional_fields_set = set(optional_fields)
    parameters_set = set(parameters)
    required = required_field_set.difference(parameters_set)
    not_needed = parameters_set.difference(required_field_set).difference(optional_fields_set)
    return list(required), list(not_needed)
