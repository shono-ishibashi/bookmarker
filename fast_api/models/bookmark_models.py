from typing import Optional, List

from pydantic import BaseModel, Field


class BookMarkSchema(BaseModel):
    # TODO: typingのFieldについて学習する
    url: str = Field(...)
    title: str = Field(...)
    memo: Optional[str] = Field(...)
    tags: Optional[List[str]] = Field(...)


# class UpdateBookmarkModel(BaseModel):
#     url: str = Field(...)
#     title: str = Field(...)
#     memo: str = Field(...)
#     tags: List[str] = Field(...)


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
