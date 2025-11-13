from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class NewTimeDelta:
    """文档指定的自定义时间段类型。

    在服务层作为业务计算使用，不直接持久化到数据库。
    """

    start_time: datetime
    end_time: datetime

    @property
    def seconds(self) -> float:
        return (self.end_time - self.start_time).total_seconds()

    def get_total_times(self, unit: str = "days") -> float:
        total_seconds = self.seconds
        if unit == "days":
            return total_seconds / 86400
        elif unit == "hours":
            return total_seconds / 3600
        elif unit == "minutes":
            return total_seconds / 60
        else:
            return total_seconds


def time_intersection(time1: NewTimeDelta, time2: NewTimeDelta) -> NewTimeDelta | None:
    """计算两个时间段交集，返回交集或 None。"""
    max_start = max(time1.start_time, time2.start_time)
    min_end = min(time1.end_time, time2.end_time)
    if max_start >= min_end:
        return None
    return NewTimeDelta(start_time=max_start, end_time=min_end)


def sum_intersections(intersections: list[NewTimeDelta | None]) -> timedelta:
    """求交集列表总时长（忽略 None）。"""
    total = timedelta(seconds=0)
    for inter in intersections:
        if inter is not None:
            total += (inter.end_time - inter.start_time)
    return total


def project_in_main_timeline(project_range: NewTimeDelta, main_range: NewTimeDelta) -> bool:
    """项目是否与主时间轴有交集。"""
    return time_intersection(project_range, main_range) is not None


def employee_available_in_secondary(employee_ranges: list[NewTimeDelta], secondary_range: NewTimeDelta) -> bool:
    """员工在副时间轴内是否仍有可用时段。

    - 逻辑：计算员工所有指派与副时间轴的交集总时长，若小于副时间轴时长，则视为可用。
    """
    intersections = [time_intersection(r, secondary_range) for r in employee_ranges]
    occupied = sum_intersections(intersections)
    required = secondary_range.end_time - secondary_range.start_time
    return occupied < required