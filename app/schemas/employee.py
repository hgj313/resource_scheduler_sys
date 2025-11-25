from pydantic import BaseModel,EmailStr
from app.services.timeline import NewTimeDelta
from .enums import RegionEnum, PositionEnum, DepartmentEnum



class EmployeeBase(BaseModel):
    name: str
    gender: str | None = None
    email: EmailStr
    phone: str | None = None
    position: PositionEnum | None = None
    department: DepartmentEnum | None = None
    region: RegionEnum | None = None


class EmployeeUpdate(BaseModel):
    name: str | None = None
    gender: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    position: PositionEnum | None = None
    department: DepartmentEnum | None = None
    region: RegionEnum | None = None

class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int

    class Config:
        from_attributes = True

class EmployeeAssign(EmployeeRead):
    assign_timeline:list[NewTimeDelta]|None=None

    class Config:
        from_attributes = True