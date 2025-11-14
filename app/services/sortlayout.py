from datetime import datetime
from pydantic import BaseModel
from .timeline import NewTimeDelta
from ..schemas.assignment import AssignmentRead
from ..schemas.layouter import LayoutRead



def get_intersection_time(x:NewTimeDelta, y:NewTimeDelta):
    """
    计算两个时间线的交集时长占比。
    """
    max_start = max(x.start_time, y.start_time)
    min_end = min(x.end_time, y.end_time)
    if max_start >= min_end:
        return 0
    return (min_end - max_start).total_seconds()

def sort_layout(main:NewTimeDelta, layouts: list[AssignmentRead]) -> float:
    """
    计算主时间线与其他时间线的交集时长占比。
    """
    proportion_list : list[LayoutRead] =[]
    main_range = main.seconds
    for layout in layouts:
        sec_timedelta = NewTimeDelta(layout.start_time,layout.end_time)
        sec_range = get_intersection_time(main,sec_timedelta)
        ratio = sec_range/main_range
        layoutread = LayoutRead(id=layout.id,name=layout.employee_name,ratio=ratio)
        proportion_list.append(layoutread)
    return proportion_list
        
        
