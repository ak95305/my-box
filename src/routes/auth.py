from flask import Blueprint
import src.controllers.auth_controller as auth_controller
import src.controllers.signup_controller as signup_controller

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['POST'])
def login_route():
    return auth_controller.login()

@auth.route("/signup", methods=['POST'])
def signup_route():
    return signup_controller.signup()

@auth.route("/verify-otp/<token>", methods=['POST'])
def verify_otp_route(token):
    return signup_controller.verify_otp(token)