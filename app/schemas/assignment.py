from pydantic import BaseModel,ConfigDict
from datetime import datetime


class AssignmentRead(BaseModel):
    id: int
    employee_name: str | None = None
    employee_id: int
    project_id: int
    start_time: datetime | None = None
    end_time: datetime | None = None
    model_config = ConfigDict(from_attributes=True)

class AssignmentUpdate(AssignmentRead):
    id: int
    employee_name: str | None = None
    employee_id: int
    project_id: int
    start_time: datetime | None = None
    end_time: datetime | None = None