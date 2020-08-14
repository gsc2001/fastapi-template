from typing import Optional, List, Dict, Union

from .base import Base
from .user import User


class ResponseBase(Base):
    success: bool = True
    error: Optional[List]
    data: Optional[Union[List, Dict[str, str]]]


class UserInResponse(ResponseBase):
    data: User


class UsersInResponse(ResponseBase):
    data: List[User] = list()


class TokenResponse(Base):
    access_token: str
    token_type: str = 'bearer'
