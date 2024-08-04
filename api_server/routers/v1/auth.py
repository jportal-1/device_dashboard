import jwt
from api_server import crud, database, schemas
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated


SECRET_KEY = "dc831f69f9f79e3a3f6968834c6a0e348d209a56b6dea487519bf31143c6972a"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

async def get_valid_user_from_token(token: Annotated[str, Depends(oauth2_scheme)],
                                    db: Annotated[Session, Depends(database.get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        data = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM],
                          options={"require": ["exp"],
                                   "verify_signature": True,
                                   "verify_exp": True})
        username = data.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    entry = crud.get_user_entry(db=db, username=username)
    if entry is None:
        raise credentials_exception
    return entry.username

def create_access_token(username: str):
    data = {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(days=7)}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def verify_credentials(db: Session, username: str, password: str):
    entry = crud.get_user_entry(db=db, username=username)
    if entry is None:
        return False
    if not verify_password(password=password, hashed_password=entry.hashed_password):
        return False
    return True

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Annotated[Session, Depends(database.get_db)]):
    if not verify_credentials(db=db, username=form_data.username, password=form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(username=form_data.username)
    return schemas.Token(access_token=access_token, token_type="bearer")

@router.get("/userinfo", response_model=str)
async def read_users_me(username: Annotated[str, Depends(get_valid_user_from_token)]):
    return username
