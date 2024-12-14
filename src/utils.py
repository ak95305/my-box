import bcrypt
import random
import string

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_hash_password(password, hashPassword):
    return bcrypt.checkpw(password.encode('utf-8'), hashPassword.encode('utf-8'))

def generate_random_string(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def generate_random_number(length=6):
    characters = string.digits
    return ''.join(random.choices(characters, k=length))

def get_bearer_token(request):
    auth_token = request.headers.get('Authorization')
    if(auth_token):
        auth_token = auth_token.split(" ")

        if(auth_token and auth_token[1] and auth_token[1] != ""):
            return auth_token[1]
        else:
            return None
    else:
        return None