from pydantic import BaseModel,EmailStr
from datetime import datetime



class ProjectBase(BaseModel):
    name: str
    value: float = 0.0
    region: str | None = None


class ProjectCreate(ProjectBase):
    start_time: datetime
    end_time: datetime


class ProjectUpdate(BaseModel):
    name: str | None = None
    value: float | None = None
    region: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class ProjectRead(ProjectBase):
    id: int
    start_time: datetime | None = None
    end_time: datetime | None = None

    class Config:
        from_attributes = True


class ProjectAssignCreate(BaseModel):
    """项目成员指派请求体。"""
    employee_id: int
    start_time: datetime
    end_time: datetime
    assign_email: EmailStr | None = None
