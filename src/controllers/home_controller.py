from flask import Response, json, Blueprint

home = Blueprint("home", __name__)

@home.route("/", methods=['GET'])
def home_route():
    return Response(
        response=json.dumps({'status': "success"}),
        status=200,
        mimetype='application/json'
    )