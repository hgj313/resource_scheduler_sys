from pydantic import BaseModel

class LayoutRead(BaseModel):
    id:int
    name:str
    ratio:float
    class Config:
        from_attributes = True