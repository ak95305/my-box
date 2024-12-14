from flask import Blueprint
import src.controllers.user_controller as user_controller

user = Blueprint("user", __name__)

@user.route("/my-profile", methods=['GET'])
def my_profile_route():
    return user_controller.my_profile()

@user.route("/logout", methods=['GET'])
def logout_route():
    return user_controller.logout()