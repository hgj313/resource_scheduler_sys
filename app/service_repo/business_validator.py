from fastapi import Request,Depends
from datetime import datetime
from fastapi.responses import JSONResponse
from ..services.timeline import NewTimeDelta,time_intersection
import sqlite3
from ..db.session import get_db

class EmployeeTimeConflictException(Exception):
    def __init__(self,assigned_task:NewTimeDelta):
        self.assigned_task = assigned_task


async def employee_time_conflict(request:Request,db:sqlite3.Connection = Depends(get_db)):
    """检查最新一次分配是否与已分配任务时间冲突"""
    cur = db.cursor()
    employee_id = request.body.get("employee_id")
    start_time = request.body.get("start_time")
    end_time = request.body.get("end_time")
    current_task = NewTimeDelta(start_time=start_time, end_time=end_time)
    #查询当前被派遣员工的所有任务
    cur.execute(
        """
        SELECT id, start_time AS assigned_start_time, end_time AS assigned_end_time FROM employee_assignments
        WHERE employee_id = ?
        """,(employee_id,)
    )
    assigned_tasks = cur.fetchall()
    #提取已经被分配的任务起始时间转化为list[NewTimeDelta]
    assigned_tasks_list = []
    for task in assigned_tasks:
        task_id = task["id"]
        assigned_start_time = datetime.fromisoformat(task["assigned_start_time"])
        assigned_end_time = datetime.fromisoformat(task["assigned_end_time"])
        assigned_task = NewTimeDelta(start_time=assigned_start_time, end_time=assigned_end_time)
        assigned_tasks_list.append(assigned_task)
    #检查冲突
    for assigned_task in assigned_tasks_list:
        if time_intersection(current_task, assigned_task) is not None:
            return JSONResponse(status_code=400, content={"detail": f"与任务 {assigned_task.id} 时间冲突"})
