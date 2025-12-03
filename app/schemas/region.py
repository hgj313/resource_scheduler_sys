from pydantic import BaseModel,ConfigDict
from .enums import RegionEnum

class RegionBase(BaseModel):
    name: RegionEnum
    location: str | None = None
    model_config = ConfigDict(from_attributes=True)


class RegionCreate(RegionBase):
    pass


class RegionUpdate(BaseModel):
    name: RegionEnum | None = None
    location: str | None = None


class RegionRead(RegionBase):
    id: int
