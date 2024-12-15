from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy.orm import Session
from models.token import ActiveToken

#Configurações do JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Cria um Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # Expiração
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#Verifica o token JWT
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_entry = db.query(ActiveToken).filter(ActiveToken.token == token).first()
    if not token_entry:
        raise HTTPException(status_code=401, detail="Token is invalid or has been revoked")
    
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Token payload invalid: 'sub' missing")
    
    return {
        "username": username,
        "is_admin": payload.get("is_admin"),
        "token": token
    }