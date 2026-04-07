from datetime import datetime, timedelta

import jwt

from bcrypt import gensalt, hashpw
from flask import current_app

import models

def _hash_password(password: str, salt=None):
    if salt is None:
        salt = gensalt();
    password_hash = hashpw(password.encode("utf-8"), salt)
    return password_hash, salt
        
def create_user_account (
    username, password, password2, first_name, last_name, email
):
    if not all([username, password, password2, first_name, last_name, email]):
        return {"error": "Missing required fields"}, 400
    if password != password2:
        return {"error": "Passwords do not match"}, 400
    if len(password) < 8:
        return {"error": "Passwords must be at least 8 characters! Dummy!"}, 400
    
    existing_user = models.UserBase.get_by_username(username)
    if existing_user:
        return {"error": "Username already exists"}, 409
    
    password_hash, salt = _hash_password(password)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    user = models.UserBase(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password_hash=password_hash.decode("utf-8"),
        password_salt=salt.decode("utf-8"),
        created_at=current_date,
    )
    user.save()
    
    return {
        "message": "User created successfully",
        "user_id": user.user_id,
        "username": user.username,
    }, 201
    
def authenticate_user(username, password):
    if not all([username, password]):
        return {"error": "Username and password are required"}, 400
    
    user = models.UserBase.get_by_username(username)
    if user is None:
        return {"error": "Invalid username or password"}, 401
    
    salt = user.password_salt.encode("utf-8")
    password_hash, _ = _hash_password(password, salt)
    
    if user.password_hash.encode("utf-8") != password_hash:
        return {"error": "Invalid username or password"}, 401
    
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        user.update_last_login(current_date)
    except Exception:
        pass
    
    return {
        "message": "Login successful",
        "user_id":user.user_id,
        "username": user.username,
    }, 200
    
def generate_token(user_id, username):
    payload = {
        "user_id": user_id,
        "username": username,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token

def verify_token(token):
    try:
        payload = jwt.decode(
            token, current_app.config['SECRET_KEY'], algorithms=["HS256"]
        )
        return payload, None
    except jwt.ExpiredSignatureError:
        print("expired")
        return None, "Token has expired"
    except jwt.InvalidTokenError as e:
        print(f"Token invalid error: {e}")
        return None, "Invalid token"