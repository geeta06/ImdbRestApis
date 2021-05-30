''' This is view file to authenticate user as admin login'''

import json
from flask import Blueprint, request
from flask import jsonify, make_response

import jwt
from datetime import datetime, timedelta

from api.models import User
from api.config.settings import Config
from api.utils.statusCodes import StatusCode
from api.utils.helpers import required_field_difference
from api.utils.validators import Validators



auth_blueprint = Blueprint("auth", __name__)
SECRET_KEY = Config.SECRET_KEY


# route for loging user in
@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    login for existing user who is admin
    :return: JsonResponse
    200 - OK
    400 - Bad Request
    500 - Internal Server Error
    """
    try:
        data = request.get_json()
        required_fields = ['username', 'password']
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
            return make_response(jsonify(
                {'message': extra_field_response}), StatusCode._400)

        # if required field not provided
        if required:
            field_missing = Validators.missing_fields_response(required)
            return make_response(jsonify(
                {'message': field_missing}), StatusCode._400)

        user = User.query \
            .filter_by(username=data.get('username')) \
            .first()

        if not user:
            # returns 400 if user does not exist
            message = "User does not exist !!"
            return make_response(jsonify(
                {'message': message}), StatusCode._400)

        if user.username == data.get('username') \
                and user.password == data.get('password'):
            # generates the JWT Token
            token = jwt.encode({
                'username': user.username,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, SECRET_KEY)

            return make_response(jsonify(
                {'token': token.decode('UTF-8')}), StatusCode._200)

        # returns 400 if password is wrong
        message = "Wrong Password !!"
        return make_response(jsonify(
            {'message': message}), StatusCode._400)
    except Exception as e:
        return make_response(jsonify(
            {'message': str(e)}), StatusCode._500)





