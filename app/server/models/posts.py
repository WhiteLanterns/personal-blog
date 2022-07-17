from typing import Optional
from pydantic import BaseModel, Field

class PostSchema(BaseModel):
    id: int
    title: str = Field(...)
    content: str = Field(...)
    date: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Crazy shit today",
                "content": "I totally ate ass, dawg",
                "date": "07/17/2022"
            }
        }


class UpdatePostSchema(BaseModel):
    id: Optional[int]
    title: Optional[str]
    content: Optional[str]
    date: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Crazy shit today",
                "content": "I totally ate ass, dawg",
                "date": "07/17/2022"
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}