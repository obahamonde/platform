from typing import *

from aioboto3 import Session
from aiohttp.web import FileField
from pydantic import BaseModel
from pydantic import Field as Data  # pylint: disable=no-name-in-module

from ..config import credentials, env
from ..schemas.models import Upload

session = Session(**credentials)


class UploadRequest(BaseModel):
    """
    UploadRequest
        - key:str
        - size:int
        - user:str
        - file:FileField
    """

    key: str = Data(...)
    size: int = Data(...)
    user: str = Data(...)
    file: FileField = Data(...)
    
    class Config:
        arbitrary_types_allowed = True


class AmazonWebServices:
    """
    Amazon Web Services
    """

    async def upload(self, request: UploadRequest):
        """
        Upload Endpoint
        """
        key, size, user, file = request.key, request.size, request.user, request.file
        async with session.client("s3") as s3:  # type: ignore
            key_ = f"{key}/{file.filename}"  # type: ignore
            await s3.put_object(
                Bucket=env.AWS_S3_BUCKET,
                Key=key_,
                Body=file.file.read(),
                ContentType=file.content_type,
                ACL="public-read",
            )
            url = f"https://s3.amazonaws.com/{env.AWS_S3_BUCKET}/{key_}"
            response = await Upload(
                user=user,
                key=key_,
                name=file.filename,
                size=size,
                type=file.content_type,
                url=url,
            ).save()
            assert isinstance(response, Upload)
            return response

