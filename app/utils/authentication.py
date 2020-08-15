from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import SECRET_KEY
from ..models.user import TokenData

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_sheme = OAuth2PasswordBearer(tokenUrl='core/login', scopes={'users': 'get users list'})


def get_access_token(data: dict, expires_in: Optional[timedelta] = timedelta(hours=2)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_in
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def verify_token(security_scopes: SecurityScopes, token: str = Depends(oauth2_sheme)) -> TokenData:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = 'Bearer'

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={
            'WWW-Authenticate': authenticate_value})
    try:
        print(token)
        print(SECRET_KEY)
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        user_id: str = payload.get('sub')
        if user_id is None:
            raise credential_exception
        token_scopes = payload.get('scopes', [])
        token_data = TokenData(user_id=user_id, scopes=token_scopes)

    except (JWTError, ValueError) as e:
        print(e)
        raise credential_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not enough permissions',
                headers={
                    'WWW-Authenticate': authenticate_value})
    return token_data
