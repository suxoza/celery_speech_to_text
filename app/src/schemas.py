
from pydantic import BaseModel, Field


class UserLoginSchema(BaseModel):
    user: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user": "paliko",
                "password": "some_simple_password"
            }
        }