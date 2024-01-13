from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import database as db

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


SECRET_KEY = '20b8170a039b4345851149b4ce331d1b6938be2eca2d43b1805291a607348deb'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


async def get_user_details(token : str = Depends(oauth2_schema)):
  
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not Validate credential",
    headers={"www-Authenticate":"Bearer"}
    )
  
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
    idNumber: str = payload.get("sub")

    if idNumber is None:
      raise credentials_exception
    
  except JWTError:
    raise credentials_exception
  
  user = await db.get_userinfo(idNumber)

  if user is None:
    raise credentials_exception
  
  return user
    



  pass
