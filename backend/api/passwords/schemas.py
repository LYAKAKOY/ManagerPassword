from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        from_attributes = True


class CreatePassword(BaseModel):
    password: str


class ShowPassword(TunedModel):
    service_name: str
    password: str
