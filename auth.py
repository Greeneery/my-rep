from datetime import datetime, timedelta

import jwt
import models
from bcrypt import gensalt, hashpw
from flask import current_app

def _hash_password(password: str, salt=None):
    if salt is None:
        salt = gensalt();
    password_hash = hashpw()