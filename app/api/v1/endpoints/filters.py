from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
import sqlite3
from typing import Annotated
from fastapi import Depends
from app.db.session import get_db
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
async def filter_projects(db: sqlite3.Connection = Depends(get_db)):
    """根据主时间轴过滤项目：返回与主时间轴有交集的项目。"""
    main = timeline_state.get_main()
    if not main:
        raise HTTPException(status_code=400, detail="Main timeline not set")

    cur = db.cursor()
    cur.execute("SELECT * FROM projects")
    results: list[ProjectRead] = []
    main_range = NewTimeDelta(main.start_time, main.end_time)
    for r in cur.fetchall():
        row = dict(r)
        
        # 使用Pydantic验证时间字段完整性
        try:
            # 如果时间字段缺失，跳过此项目
            if not (row.get("start_time") or row.get("end_time")):
                continue
                
            # 时间完整的项目进行时间范围比较
            pj_range = NewTimeDelta(datetime.fromisoformat(row["start_time"]), datetime.fromisoformat(row["end_time"]))
            if project_in_main_timeline(pj_range, main_range):
                # 转换为响应模型
                project_data = {
                    "id": row["id"],
                    "name": row["name"],
                    "value": row["value"],
                    "region": row.get("region"),
                    "start_time": datetime.fromisoformat(row["start_time"]) if row.get("start_time") else None,
                    "end_time": datetime.fromisoformat(row["end_time"]) if row.get("end_time") else None
                }
                results.append(ProjectRead(**project_data))
                
        except (ValueError, TypeError):
            # 时间格式无效或转换错误，跳过此项目
            continue
    return results


@router.get("/employees", response_model=list[EmployeeAssign])
async def filter_employees(region: str | None = Query(default=None), db: sqlite3.Connection = Depends(get_db)):
    """根据副时间轴过滤员工：返回在副时间轴内仍有可用时段的员工。"""
    sec = timeline_state.get_secondary()
    if not sec:
        raise HTTPException(status_code=400, detail="Secondary timeline not set")

    secondary_range = NewTimeDelta(sec.start_time, sec.end_time)

    # 使用LEFT JOIN获取员工信息及项目指派信息
    cur = db.cursor()
    if region:
        cur.execute("""
            SELECT e.*, ea.project_id, ea.start_time as assign_start_time, ea.end_time as assign_end_time
            FROM employees e
            LEFT JOIN employee_assignments ea ON e.id = ea.employee_id
            WHERE e.region = ?
        """, (region,))
    else:
        cur.execute("""
            SELECT e.*, ea.project_id, ea.start_time as assign_start_time, ea.end_time as assign_end_time
            FROM employees e
            LEFT JOIN employee_assignments ea ON e.id = ea.employee_id
        """)
    
    rows = cur.fetchall()
    
    # 在应用层对结果进行分组和聚合
    # 将同一个员工的多条记录合并，构建assign_timeline列表
    employee_dict: dict[int, dict] = {}
    for row in rows:
        r = dict(row)
        employee_id = r["id"]
        
        if employee_id not in employee_dict:
            # 初始化员工信息
            employee_dict[employee_id] = {
                "id": r["id"],
                "name": r["name"],
                "gender": r["gender"],
                "email": r["email"],
                "phone": r["phone"],
                "position": r["position"],
                "department": r["department"],
                "region": r["region"],
                "assign_timeline": []
            }
        
        # 如果有项目指派信息，则添加到assign_timeline列表中
        if r["project_id"] is not None:
            assign_timeline_entry = NewTimeDelta(
                datetime.fromisoformat(r["assign_start_time"].replace("Z","+00:00")) if r["assign_start_time"] else None,
                datetime.fromisoformat(r["assign_end_time"].replace("Z","+00:00")) if r["assign_end_time"] else None)
            employee_dict[employee_id]["assign_timeline"].append(assign_timeline_entry)
    
    # 转换为EmployeeAssign对象列表
    results: list[EmployeeAssign] = []
    for emp_data in employee_dict.values():
        emp_data.pop
        assign_ranges = emp_data["assign_timeline"]
        # 检查员工在副时间轴内是否仍有可用时段
        if employee_available_in_secondary(assign_ranges, secondary_range):
            print(emp_data)
            print("----------------------------------------------------------------")
            results.append(EmployeeAssign(**emp_data))
    
    return results
