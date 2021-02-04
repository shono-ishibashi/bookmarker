from typing import Optional

from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId


class UserSchema(BaseModel):
    # _id: ObjectId
    name: str = Field(...)
    email: str = EmailStr(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example ": {
                "name": "タロー",
                "email": "example@example.com",
                "password": "password"
            }
        }


class UpdateUserModel(BaseModel):
    name: str = Optional[str]
    email: str = Optional[EmailStr]
    password: str = Optional[str]

    class Config:
        schema_extra = {
            "example ": {
                "name": "タロー",
                "email": "example@example.com",
                "password": "password"
            }
        }


def response_model(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }


def error_response_model(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
