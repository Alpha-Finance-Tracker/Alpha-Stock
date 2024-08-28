from datetime import datetime
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from jose import jwt, JWTError

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

async def verify_token(token: str):
    print(token)
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get('exp')
        if exp is None or datetime.fromtimestamp(exp) < datetime.now():
            raise credentials_exception
        print(payload)
        return payload
    except JWTError:
        print('ERROR')
        raise credentials_exception

