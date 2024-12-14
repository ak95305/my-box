from flask import Response, json, request
from src.models.user import User

def login():
    data = request.get_json()
    user = User.attemptLogin(data['username'], data['password'])
    
    if(user):
        User.makeSession(user)

        return Response(
            response=json.dumps({
                'status': True, 
                "message": 'Login Successfully!',
                "data": user.to_dict(),
            }),
            status=200,
            mimetype='application/json'
        )
    else:
        return Response(
            response=json.dumps({'status': False, "message": 'Invalid Credentials!'}),
            status=403,
            mimetype='application/json'
        )