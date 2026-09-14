from database import engine, get_db
import models
import schemas
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({
        "exp" : expire
    })

    token = jwt.encode(to_encode, os.getenv("SECRET_KEY"),os.getenv("ALGORITHM"))
    return token
