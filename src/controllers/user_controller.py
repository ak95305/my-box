from flask import Response, json, request
from src.models.user import User

def my_profile():
    return Response(
        response=json.dumps({
            'status': True, 
            "message": 'Data Fetched Successfully!',
        }),
        status=200,
        mimetype='application/json'
    )


def logout():
    logout = User.removeSession()

    if(logout):
        return Response(
            response=json.dumps({
                "status": True,
                "message": "Logout Successfully!",
            }),
            status=200,
            mimetype='application/json'
        )
    else:
        return Response(
            response=json.dumps({
                "status": False,
                "message": "Something Went Wrong!",
            }),
            status=400,
            mimetype='application/json'
        )