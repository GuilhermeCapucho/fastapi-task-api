from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models.user import User
from models.token import ActiveToken
from auth.jwt_handler import create_access_token, get_current_user

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Model de registro
class RegisterInput(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, description="Username must be 5-20 characters long")
    password: str = Field(..., min_length=5, description="Password must be at least 5 characters long")
    email: str
    is_admin: bool = False

#Model de login
class LoginInput(BaseModel):
    username: str
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

#Rota de registro
@router.post("/register")
def register(input: RegisterInput, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == input.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=input.username,
        hashed_password=hash_password(input.password),
        email=input.email,
        is_admin=input.is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user": {"username": new_user.username, "is_admin": new_user.is_admin}}

#Rota de login
@router.post("/login")
def login(input: LoginInput, db: Session = Depends(get_db)):
    user = authenticate_user(input.username, input.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username, "is_admin": user.is_admin})
    
    token_entry = ActiveToken(token=access_token)
    db.add(token_entry)
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer"}

#Rota de logout
@router.post("/logout")
def logout(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    token_entry = db.query(ActiveToken).filter(ActiveToken.token == current_user["token"]).first()
    if not token_entry:
        raise HTTPException(status_code=404, detail="Token not found")
    
    db.delete(token_entry)
    db.commit()
    return {"message": "Logout successful"}