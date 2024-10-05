from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, database, database_models, app_settings
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

settings = app_settings.get_settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(
        f"This the Encoded JWT Token with the user_id and token expiry date: {encoded_jwt}"
    )
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenicate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)

    user = (
        db.query(database_models.Users)
        .filter(database_models.Users.id == token.id)
        .first()
    )
    return user


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = str(payload.get("user_id"))
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)

    except JWTError as e:
        print(f"The exception has occured {e}")
        raise credentials_exception
    return token_data
