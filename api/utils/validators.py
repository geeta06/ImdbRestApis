'''This file is used to write validators related to projects'''

class InputOutOfBounds(Exception):
    """
    exception in case of value is out of defined limit
    """
    pass

class Validators():
    """
    This class handles validators which can be reused in project
    """

    @staticmethod
    def missing_fields_response(list_of_missing_fields):
        """
        generate the response for missing fields
        :param list_of_missing_fields: list_of_missing_fields
        :return: Response for missing fields
        """
        if len(list_of_missing_fields) == 1:
            response = "{} field is missing".format(
                list_of_missing_fields[0])
            return response
        else:
            missing_fields = ", ".join(list_of_missing_fields)
            response = "{} field are missing".format(missing_fields)
            return response


    @staticmethod
    def extra_fields_response(list_of_extra_fields):
        """
        generate the response for extra fields
        :param list_of_extra_fields: list_of_extra_fields
        :return: Response for extra fields
        """
        if len(list_of_extra_fields) == 1:
            response = "{} field is not needed".format(
                list_of_extra_fields[0])
            return response
        else:
            extra_fields = ", ".join(list_of_extra_fields)
            response = "{} field are not needed".format(
                extra_fields)
            return response


    @staticmethod
    def param_validation(popularity, imdb_score):
        """
        this function used to check if popularity and imdb score
        value is in valid range or not
        :param popularity: popularity of movie model
        :return: str message
        """
        if popularity < 0 or popularity > 100:
            raise InputOutOfBounds

        if imdb_score < 0 or imdb_score > 10:
            raise InputOutOfBounds

