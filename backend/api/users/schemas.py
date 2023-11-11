import uuid

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        from_attributes = True


class CreateUser(BaseModel):
    login: str
    password: str


class UpdateUser(BaseModel):
    login: str
    password: str


class ShowUser(TunedModel):
    user_id: uuid.UUID


class Token(BaseModel):
    access_token: str
    token_type: str
