from datetime import datetime
from pydantic import BaseModel, field_validator


class TimeRange(BaseModel):
    """时间范围模式对象，作为 NewTimeDelta 的API等价表示。

    - start_time: 开始时间
    - end_time: 结束时间
    """

    start_time: datetime
    end_time: datetime

    @field_validator("end_time")
    @classmethod
    def validate_order(cls, v: datetime, info):
        start = info.data.get("start_time")
        if start and v <= start:
            raise ValueError("end_time must be greater than start_time")
        return v