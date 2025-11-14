from pydantic import BaseModel
from datetime import datetime

class LayoutRead(BaseModel):
    id:int
    name:str
    start_point_ratio:float
    ratio:float
    class Config:
        from_attributes = True

class LayoutProject(BaseModel):
    project_id_list:list[int]
    main_start_time:datetime
    main_end_time:datetime

class LayoutProjectRead(BaseModel):
    project_id:int
    project_name:str
    start_point_ratio:float
    project_ratio:float
    class Config:
        from_attributes = True
