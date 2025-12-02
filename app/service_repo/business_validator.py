from fastapi import Request,Depends
from datetime import datetime
from fastapi.responses import JSONResponse
from ..services.timeline import NewTimeDelta,time_intersection
from sqlalchemy.orm import Session
from ..db.session import get_session
from sqlalchemy import select
from ..db.models import EmployeeAssignment

class EmployeeTimeConflictException(Exception):
    def __init__(self,assigned_task:NewTimeDelta):
        self.assigned_task = assigned_task


async def employee_time_conflict(request:Request, session: Session = Depends(get_session)):
    """检查最新一次分配是否与已分配任务时间冲突"""
    employee_id = request.body.get("employee_id")
    start_time = request.body.get("start_time")
    end_time = request.body.get("end_time")
    current_task = NewTimeDelta(start_time=start_time, end_time=end_time)
    #查询当前被派遣员工的所有任务
    assigned_tasks = session.execute(select(EmployeeAssignment).where(EmployeeAssignment.employee_id == employee_id)).scalars().all()
    #提取已经被分配的任务起始时间转化为list[NewTimeDelta]
    assigned_tasks_list = []
    for task in assigned_tasks:
        task_id = task.id
        assigned_start_time = datetime.fromisoformat(task.start_time)
        assigned_end_time = datetime.fromisoformat(task.end_time)
        assigned_task = NewTimeDelta(start_time=assigned_start_time, end_time=assigned_end_time)
        assigned_tasks_list.append(assigned_task)
    #检查冲突
    for assigned_task in assigned_tasks_list:
        if time_intersection(current_task, assigned_task) is not None:
            return JSONResponse(status_code=400, content={"detail": f"与任务 {assigned_task.id} 时间冲突"})
