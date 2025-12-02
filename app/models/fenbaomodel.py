from typing import Annotated
from fastapi import Depends,FastAPI,HTTPException,Query
from sqlmodel import SQLModel,Field,Session,create_engine,select
from app.schemas.project import ProjectBase

class Fenbao(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)
    name:str = Field(index=True)
    professional:str = Field(index=True)
    staff_count:int = Field(index=True)
    project_in:list[ProjectBase] = Relationship(back_populates = "fenbao",link_model = FenbaoProject)
 