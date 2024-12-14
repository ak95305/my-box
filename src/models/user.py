from flask import request
from sqlalchemy import select
from src import session
from datetime import datetime, timedelta

from src.entity.user import UserEntity
from src.models.user_token import UserToken

import src.utils as utils

class User(UserEntity):
    def get(id):
        try:
            stmt = (
                select(User)
                .where(User.id == id)
            )
            user_token = session.scalars(stmt).one()
            return user_token

        except Exception as e:
            return False
        
    
    def attemptLogin(username, password):
        try:
            stmt = (
                select(User)
                .where(User.username == username)
            )
            user = session.scalars(stmt).one()
            
            if(user):
                if(utils.check_hash_password(password, user.password)):
                    return user
                else:
                    return False
            else:
                return False
                    

        except Exception as e:
            return False
        
    
    def makeSession(user):
        user_token = UserToken.getRowUserId(user.id)

        if(user_token):
            user_token.token = utils.generate_random_string(32)
            user_token.expires_at = datetime.now() + timedelta(days=1)
        else:
            user_token = UserToken(
                user_id=user.id,
                token=utils.generate_random_string(),
                expires_at=datetime.now() + timedelta(days=1)
            )
            session.add(user_token)

        session.commit()
        return True

    
    def getLoginUser():
        auth_token = utils.get_bearer_token(request)
        if(auth_token):
            user_token = UserToken.getRow(auth_token)

            if(user_token and user_token.user_id):
                user = User.get(user_token.user_id)

                if(user):
                    return user
                else:
                    return None
            else:
                return None
        else:
            return None
        
    
    def removeSession():
        auth_token = utils.get_bearer_token(request)
        
        if(auth_token):
            user_token = UserToken.getRow(auth_token)
            
            session.delete(user_token)
            session.commit()
            
            return True
        else:
            return None