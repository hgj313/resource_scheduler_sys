from textwrap import indent
from pydantic import BaseModel,ConfigDict

class FenBaoBase(BaseModel):
    name:str
    professional:str
    staff_count:int
    level:str
    model_config = ConfigDict(from_attributes=True)

class FenBaoCreate(FenBaoBase):
    pass

class FenBaoRead(FenBaoBase):
    id:int

class FenBaoUpdate(FenBaoBase):
    name:str|None = None
    professional:str|None = None
    staff_count:int|None = None
    level:str|None = None
