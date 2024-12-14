from flask import request, Response, json
from src.models.user_token import UserToken
from datetime import datetime, timedelta
from src import session

import src.utils as utils

def user_auth():
    auth_token = utils.get_bearer_token(request)
    
    if(auth_token):
        user_token = UserToken.getRow(auth_token)

        if(user_token and user_token.expires_at > datetime.now()):
            user_token.expires_at = datetime.now() + timedelta(days=1)
            session.commit()

            return None
        else:
            return Response(
            response=json.dumps({
                'status': False, 
                "message": 'Session Expired!',
            }),
            status=403,
            mimetype='application/json'
        )
    else:
        return Response(
            response=json.dumps({
                'status': False, 
                "message": 'Forbidden',
            }),
            status=401,
            mimetype='application/json'
        )