from fastapi import APIRouter, Depends, HTTPException,Body
import sqlite3
from datetime import datetime
from app.db.session import get_db
from app.schemas.assignment import AssignmentRead
from app.services.sortlayout import sort_layout_user,sort_layout_project
from app.services.timeline import NewTimeDelta,project_in_main_timeline
from app.schemas.layouter import LayoutRead,LayoutProject,LayoutProjectRead

router = APIRouter(tags=["layout"],prefix="/layout")

@router.get("/{project_id}",response_model=list[LayoutRead])
def get_layout_ratio(project_id:int,db:sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("""
    SELECT e.name,ea.* FROM 
    employee_assignments ea
    JOIN employees e ON ea.employee_id = e.id
    WHERE ea.project_id = ?
    """,(project_id,))
    rows = cur.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="No layout found for this project")
    layout_ratio_list = []
    for row in rows:
        assignment=AssignmentRead(
            id = row["id"],
            employee_name = row["name"],
            employee_id = row["employee_id"],
            project_id = row["project_id"],
            start_time = datetime.fromisoformat(row["start_time"]),
            end_time = datetime.fromisoformat(row["end_time"]),
        )
        layout_ratio_list.append(assignment)

    cur.execute("""
    SELECT start_time,end_time FROM projects WHERE id = ?
    """,(project_id,))
    project = cur.fetchone()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_range = NewTimeDelta(
        start_time = datetime.fromisoformat(project["start_time"]),
        end_time = datetime.fromisoformat(project["end_time"])
    )
    proportion_list = sort_layout_user(project_range,layout_ratio_list)
    return proportion_list

    
@router.post("/{region}",response_model=list[LayoutProjectRead])
def get_layout_ratio(region:str|None = None,payload:LayoutProject=Body(...,description=" Contain project_id and main_timeline"),db:sqlite3.Connection = Depends(get_db)):
    main_start_time = payload.main_start_time
    main_end_time = payload.main_end_time
    main_range = NewTimeDelta(main_start_time,main_end_time)
    cur = db.cursor()
    placeholder = ",".join(["?"]*len(payload.project_id_list))
    SQLR = f"SELECT * FROM projects WHERE region = ? AND id IN({placeholder})"
    SQL = f"SELECT * FROM projects WHERE id IN({placeholder})"
    if region and region != "all":
        cur.execute(SQLR,(region,*payload.project_id_list))
    else:
        cur.execute(SQL,(*payload.project_id_list,))
    rows = cur.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Project not found")
    project_layout_ratio_list = []
    for row in rows:
        start_time = datetime.fromisoformat(row["start_time"])
        end_time = datetime.fromisoformat(row["end_time"])
        layout_range = NewTimeDelta(start_time,end_time)
        start_point_ratio,project_ratio = sort_layout_project(main_range,layout_range)
        layoutprojectread = LayoutProjectRead(
            project_id = row["id"],
            project_name = row["name"],
            start_point_ratio = start_point_ratio,
            project_ratio = project_ratio,
        )
        project_layout_ratio_list.append(layoutprojectread)
    return project_layout_ratio_list
    
