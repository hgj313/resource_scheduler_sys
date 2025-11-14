from fastapi import APIRouter, Depends, HTTPException,Query
import sqlite3
from typing import Annotated
from datetime import datetime
from app.db.session import get_db
from app.schemas.assignment import AssignmentRead
from app.services.sortlayout import sort_layout
from app.services.timeline import NewTimeDelta,project_in_main_timeline
from app.schemas.layouter import LayoutRead

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
    proportion_list = sort_layout(project_range,layout_ratio_list)
    return proportion_list

    
@router.get("/{region}",response_model=list[dict])
def get_layout_ratio(region:str,start_time:datetime = Query(...),end_time:datetime = Query(...),db:sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()

    cur.execute("""
    SELECT * FROM projects WHERE 
    """,(region,))
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
    proportion_list = sort_layout(project_range,layout_ratio_list)
    return proportion_list
        
        

