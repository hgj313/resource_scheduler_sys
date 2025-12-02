from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated
from fastapi import Depends
from app.dependencies import get_filter_repo
from app.repositories.interfaces import IFilterRepository
from app.schemas import ProjectRead
from app.schemas.employee import EmployeeAssign,EmployeeRead
from app.services.timeline import NewTimeDelta, employee_available_in_secondary, project_in_main_timeline
from app.state.timelines import timeline_state
from app.services.datatransform import transform_date


router = APIRouter(tags=["filters"], prefix="/filters")


@router.put("/main-timeline")
def set_main_timeline(
    start: Annotated[datetime ,Query()],
    end: Annotated[datetime ,Query()]
    ):
    """设置主时间轴。"""
    timeline_state.set_main(start, end)
    return {"ok": True}


@router.put("/secondary-timeline")
def set_secondary_timeline(
    start: datetime = Query(), 
    end: datetime = Query()
    ):
    """设置副时间轴。"""
    timeline_state.set_secondary(start, end)
    return {"ok": True}


@router.get("/projects", response_model=list[ProjectRead])
async def filter_projects(region:str | None = Query(default=None), repo: IFilterRepository = Depends(get_filter_repo)):
    """根据主时间轴过滤项目：返回与主时间轴有交集的项目。"""
    main = timeline_state.get_main()
    if not main:
        raise HTTPException(status_code=400, detail="Main timeline not set")
    
    main_range = NewTimeDelta(main.start_time, main.end_time)
    return await repo.filter_projects(main_range, region)


@router.get("/employees", response_model=list[EmployeeAssign])
async def filter_employees(region: str | None = Query(default=None), repo: IFilterRepository = Depends(get_filter_repo)):
    """根据副时间轴过滤员工：返回在副时间轴内仍有可用时段的员工。"""
    sec = timeline_state.get_secondary()
    if not sec:
        raise HTTPException(status_code=400, detail="Secondary timeline not set")

    secondary_range = NewTimeDelta(sec.start_time, sec.end_time)

    return await repo.filter_employees(secondary_range, region)
