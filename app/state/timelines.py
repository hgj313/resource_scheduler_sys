from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TimeRangeState:
    start_time: datetime
    end_time: datetime


class TimelineState:
    """全局时间轴内存状态。

    - main_timeline: 主时间轴
    - secondary_timeline: 副时间轴（可选）
    """

    def __init__(self) -> None:
        self._main: Optional[TimeRangeState] = None
        self._secondary: Optional[TimeRangeState] = None

    def set_main(self, start: datetime, end: datetime) -> None:
        if end <= start:
            raise ValueError("main timeline end must be greater than start")
        self._main = TimeRangeState(start, end)

    def set_secondary(self, start: datetime, end: datetime) -> None:
        if end <= start:
            raise ValueError("secondary timeline end must be greater than start")
        self._secondary = TimeRangeState(start, end)

    def get_main(self) -> Optional[TimeRangeState]:
        # 返回私有属性的副本，避免外部直接修改内部状态
        return TimeRangeState(self._main.start_time, self._main.end_time) if self._main else None

    def get_secondary(self) -> Optional[TimeRangeState]:
        # 返回私有属性的副本，避免外部直接修改内部状态
        return TimeRangeState(self._secondary.start_time, self._secondary.end_time) if self._secondary else None


timeline_state = TimelineState()