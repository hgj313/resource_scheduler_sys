from textwrap import indent
from pydantic import BaseModel,ConfigDict,Field

class FenBaoBase(BaseModel):
    name:str = Field(...,min_length=1,strip_whitespace=True)
    professional:str = Field(...,min_length=1,strip_whitespace=True)
    staff_count:int = Field(...,ge=1)
    level:str = Field(...,min_length=1,strip_whitespace=True)
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
