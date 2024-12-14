from sqlalchemy import select

from src.entity.user_token import UserTokenEntity
from src import session

class UserToken(UserTokenEntity):
    def create(data):
        record = UserToken(data)
        session.add(record)
        session.commit()

    def get(id):
        try:
            stmt = (
                select(UserToken)
                .where(UserToken.id == id)
            )
            user_token = session.scalars(stmt).one()
            return user_token

        except Exception as e:
            return False

    def getRow(token):
        try:
            stmt = (
                select(UserToken)
                .where(UserToken.token == token)
            )
                
            user_token = session.scalars(stmt).one()
            return user_token

        except Exception as e:
            return False

    def getRowUserId(id):
        try:
            stmt = (
                select(UserToken)
                .where(UserToken.user_id == id)
            )
                
            user_token = session.scalars(stmt).one()
            return user_token

        except Exception as e:
            return False