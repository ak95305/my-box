from flask import request
from sqlalchemy import select
from src import session
from datetime import datetime, timedelta

from src.entity.user import UserEntity
from src.models.user_token import UserToken

import src.utils as utils

class User(UserEntity):
    def __init__(self, data):
        super().__init__(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email'),
            disk_storage=data.get('disk_storage'),
            token=data.get('token'),
            otp=data.get('otp')
        )


    def create(data):
        data['username'] = data['first_name'] + "-" + data['last_name'] + "-" + utils.generate_random_string(5)
        data['password'] = utils.hash_password(data['password'])
        data['token'] = utils.generate_random_string(32)
        data['otp'] = utils.generate_random_number()

        record = User(data)

        try:
            session.add(record)
            session.commit()

            return record
        except Exception as e:
            return None


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
        
    
    def getRow(where):
        try:
            stmt = select(User)

            for key, value in where.items():
                stmt = stmt.where(getattr(User, key) == value)
                
            record = session.scalars(stmt).one_or_none()
            return record if record else False

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