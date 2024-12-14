from flask import Blueprint
import src.controllers.auth_controller as auth_controller

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['POST'])
def login_route():
    return auth_controller.login()