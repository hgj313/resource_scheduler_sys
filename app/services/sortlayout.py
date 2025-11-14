from datetime import datetime
from pydantic import BaseModel
from .timeline import NewTimeDelta
from ..schemas.assignment import AssignmentRead
from ..schemas.layouter import LayoutProjectRead, LayoutRead



def get_intersection_time(x:NewTimeDelta, y:NewTimeDelta):
    """
    计算两个时间线的交集时长占比。
    """
    max_start = max(x.start_time, y.start_time)
    min_end = min(x.end_time, y.end_time)
    if max_start >= min_end:
        return 0
    return (min_end - max_start).total_seconds()

def sort_layout_user(main:NewTimeDelta, layouts: list[AssignmentRead]) -> float:
    """
    计算主时间线与其他时间线的交集时长占比。
    """
    proportion_list : list[LayoutRead] =[]
    main_range = main.seconds
    for layout in layouts:
        intersec_timedelta = NewTimeDelta(layout.start_time,layout.end_time)
        sec_range = get_intersection_time(main,intersec_timedelta)
        ratio = sec_range/main_range
        start_point_ratio = get_layout_start_point(main,intersec_timedelta)
        layoutread = LayoutRead(
            id=layout.id,
            name=layout.employee_name,
            start_point_ratio=start_point_ratio,
            ratio=ratio,
            )
        proportion_list.append(layoutread)
    return proportion_list

def sort_layout_project(main:NewTimeDelta, layout_range:NewTimeDelta) -> float:
    """
    计算主时间线与其他时间线的交集时长占比。
    """
    main_range = main.seconds
    intersec_range = get_intersection_time(main,layout_range)
    ratio = intersec_range/main_range
    start_point_ratio = get_layout_start_point(main,layout_range)
    return start_point_ratio,ratio

def get_layout_start_point(base_delta:NewTimeDelta,em_delta:NewTimeDelta):
    """
    计算用户在项目时间线上的开始时间点。
    """
    if em_delta.start_time < base_delta.start_time:
        start=base_delta.start_time
    else:
        start=em_delta.start_time
    start_point_ratio = (start - base_delta.start_time).total_seconds()/base_delta.seconds
    return start_point_ratio
        
        
