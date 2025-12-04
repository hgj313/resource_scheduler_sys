from textwrap import indent
from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field
from typing import Annotated

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
    available_staff_count:int | None = None

class FenBaoUpdate(FenBaoBase):
    name:str|None = None
    professional:str|None = None
    staff_count:int|None = None
    available_staff_count:int|None = None
    level:str|None = None

class FenbaoTeam(BaseModel):
    leader_name:str | None
    company_name:str
    team_number:int
    project_at_id : Annotated[int, Field(gt=0)]
    start_time:datetime
    end_time:datetime 
    level:str | None
    belong_to_fenbao_id:int
    status:str | None = "assigned"
    model_config = ConfigDict(from_attributes=True)

class FenbaoTeamRead(FenbaoTeam):
    id:int
    project_name:str | None = None

class FenbaoTeamUpdate(FenbaoTeam):
    leader_name:str | None
    company_name:str | None
    team_number:int | None
    project_at_id : Annotated[int, Field(gt=0)] | None
    start_time:datetime | None
    end_time:datetime | None
    level:str | None
    belong_to_fenbao_id:int
    status:str | None = None
