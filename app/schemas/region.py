from pydantic import BaseModel


class RegionBase(BaseModel):
    name: str
    location: str | None = None


class RegionCreate(RegionBase):
    pass


class RegionUpdate(BaseModel):
    name: str | None = None
    location: str | None = None


class RegionRead(RegionBase):
    id: int

    class Config:
        from_attributes = True