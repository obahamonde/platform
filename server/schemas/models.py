from datetime import datetime
from typing import *

from aiofauna import BaseModel
from aiofauna import FaunaModel as Model
from aiofauna import Field as Data
from urllib3 import response

from ..templates import Context

Scalar = Union[str, int, float, bool, None]


class User(Model):
    """
    Auth0 User, Github User or Cognito User
    """

    email: Optional[str] = Data(default=None, index=True)
    email_verified: Optional[bool] = Data(default=False)
    family_name: Optional[str] = Data(default=None)
    given_name: Optional[str] = Data(default=None)
    locale: Optional[str] = Data(default=None, index=True)
    name: str = Data(...)
    nickname: Optional[str] = Data(default=None)
    picture: Optional[str] = Data(default=None)
    sub: str = Data(..., unique=True)
    updated_at: Optional[str] = Data(default=None)
    source: Literal["auth0", "github", "cognito"] = Data(default="auth0", index=True)

class ChatGpt(Model):
    """

    Chat

    """

    user: str = Data(..., description="User reference", index=True)
    prompt:str = Data(..., description="Prompt message")
    response: str = Data(..., description="Response message")
    context: List[Context] = Data(..., description="Context")
    tokens: int = Data(..., description="Tokens")
             
class Upload(Model):
    """

    S3 Upload Record

    """

    user: str = Data(..., description="User sub", index=True)
    name: str = Data(..., description="File name")
    key: str = Data(..., description="File key", unique=True)
    size: int = Data(..., description="File size", gt=0)
    type: str = Data(..., description="File type", index=True)
    lastModified: float = Data(
        default_factory=lambda: datetime.now().timestamp(),
        description="Last modified",
        index=True,
    )
    url: Optional[str] = Data(None, description="File url")