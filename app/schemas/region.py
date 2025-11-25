from pydantic import BaseModel
from .enums import RegionEnum

class RegionBase(BaseModel):
    name: RegionEnum
    location: str | None = None

class RegionCreate(RegionBase):
    pass


class RegionUpdate(BaseModel):
    name: RegionEnum | None = None
    location: str | None = None


class RegionRead(RegionBase):
    id: int

    class Config:
        from_attributes = True