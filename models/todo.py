from beanie import Document
from fastapi import Form
from pydantic import BaseModel


class Todo(Document):
    title: str
    description: str

    class Config:
        schema_extra = {
            "example": {
                "title": "",
                "description": ""
            }
        }

    @classmethod
    def as_form(cls, title: str = Form(...), description: str = Form(...)):
        return cls(title=title, description=description)
