#JWT token verfication file for user as admin
import jwt
from flask import jsonify, request, make_response
from functools import wraps

from api.models import User
from api.config.settings import Config
from .statusCodes import StatusCode


SECRET_KEY = Config.SECRET_KEY

# decorator for verifying the JWT
def admin_jwt_token_required(func):
    """
    this function is used to verify logged in user's token
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 400 if token is not passed
        if not token:
            return make_response(jsonify({'message': 'Token is missing !!'}), StatusCode._400)

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, SECRET_KEY)
            current_user = User.query \
                .filter_by(username=data['username']) \
                .first()
        except:
            return make_response(jsonify({
                'message': 'Token is invalid !!'
            }), StatusCode._400)
        # returns the current logged in users contex to the routes
        return func(*args, **kwargs)

    return decorated
