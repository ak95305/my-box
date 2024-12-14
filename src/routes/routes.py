from flask import Blueprint
from src.routes.auth import auth
from src.routes.users import user
from src.middleware.user_auth import user_auth

api = Blueprint('api', __name__)

api.register_blueprint(auth)
api.register_blueprint(user)


@user.before_request
def user_auth_middleware():
    return user_auth()