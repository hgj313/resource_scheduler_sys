from pydantic import BaseModel
from datetime import datetime


class AssignmentRead(BaseModel):
    id: int
    employee_name: str | None = None
    employee_id: int
    project_id: int
    start_time: datetime | None = None
    end_time: datetime | None = None

    class Config:
        from_attributes = True