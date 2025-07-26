# models/base.py
from pydantic import BaseModel, Extra

class ImmutableBaseModel(BaseModel):
    class Config:
        frozen = True
        extra = Extra.forbid