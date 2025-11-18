from datetime import datetime,timezone
from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from app.db.session import get_db
from app.schemas import ProjectCreate, ProjectUpdate, ProjectRead, ProjectAssignCreate, AssignmentRead
from app.services.scheduler import schedule_assignment_notifications

router = APIRouter(tags=["projects"], prefix="/projects")


@router.post("/", response_model=ProjectRead)
def create_project(payload: ProjectCreate, db: sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()
    d = payload.model_dump()
    
    # Check if a project with the same name and value already exists
    cur.execute(
        "SELECT * FROM projects WHERE name = ? AND value = ?",
        (d.get("name"), d.get("value", 0.0))
    )
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Project with this name and value already exists")
    
    try:
        cur.execute(
            """
            INSERT INTO projects (name, value, region, start_time, end_time)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                d.get("name"),
                d.get("value", 0.0),
                d.get("region"),
                d.get("start_time").isoformat() if d.get("start_time") else None,
                d.get("end_time").isoformat() if d.get("end_time") else None,
            ),
        )
        db.commit()
        pid = cur.lastrowid
        cur.execute("SELECT * FROM projects WHERE id = ?", (pid,))
        row = dict(cur.fetchone())
        if row.get("start_time"):
            row["start_time"] = datetime.fromisoformat(row["start_time"])
        if row.get("end_time"):
            row["end_time"] = datetime.fromisoformat(row["end_time"])
        return ProjectRead(**row)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Project with this name and value already exists")


@router.get("/", response_model=list[ProjectRead])
def list_projects(db: sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM projects")
    rows = []
    for r in cur.fetchall():
        row = dict(r)
        if row.get("start_time"):
            row["start_time"] = datetime.fromisoformat(row["start_time"])
        if row.get("end_time"):
            row["end_time"] = datetime.fromisoformat(row["end_time"])
        rows.append(ProjectRead(**row))
    return rows


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    r = cur.fetchone()
    if not r:
        raise HTTPException(status_code=404, detail="Project not found")
    row = dict(r)
    if row.get("start_time"):
        row["start_time"] = datetime.fromisoformat(row["start_time"])
    if row.get("end_time"):
        row["end_time"] = datetime.fromisoformat(row["end_time"])
    return ProjectRead(**row)


@router.put("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, payload: ProjectUpdate, db: sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Project not found")
    updates = payload.model_dump(exclude_unset=True)
    if updates:
        set_clauses = []
        values = []
        for k, v in updates.items():
            if k in ("start_time", "end_time") and v is not None:
                v = v.isoformat()
            set_clauses.append(f"{k} = ?")
            values.append(v)
        values.append(project_id)
        sql = f"UPDATE projects SET {', '.join(set_clauses)} WHERE id = ?"
        cur.execute(sql, tuple(values))
        db.commit()
    cur.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    r = cur.fetchone()
    row = dict(r)
    if row.get("start_time"):
        row["start_time"] = datetime.fromisoformat(row["start_time"])
    if row.get("end_time"):
        row["end_time"] = datetime.fromisoformat(row["end_time"])
    return ProjectRead(**row)


@router.delete("/{project_id}")
def delete_project(project_id: int, db: sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    db.commit()
    return {"deleted": True}


@router.post("/{project_id}/assignments", response_model=AssignmentRead)
def assign_employee(project_id: int, payload: ProjectAssignCreate, db: sqlite3.Connection = Depends(get_db)):
    """为项目指派员工及其时间段（拖曳分配的接口形态）。"""
    cur = db.cursor()
    # 校验项目与员工存在
    cur.execute("SELECT id FROM projects WHERE id = ?", (project_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Project not found")
    cur.execute("SELECT id FROM employees WHERE id = ?", (payload.employee_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Employee not found")

    if payload.end_time <= payload.start_time:
        raise HTTPException(status_code=400, detail="end_time must be greater than start_time")

    cur.execute(
        """
        INSERT INTO employee_assignments (employee_id, project_id, start_time, end_time, assigner_email)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            payload.employee_id,
            project_id,
            payload.start_time.isoformat(),
            payload.end_time.isoformat(),
            payload.user_email,
        ),
    )
    db.commit()
    aid = cur.lastrowid
    cur.execute("SELECT * FROM employee_assignments WHERE id = ?", (aid,))
    r = dict(cur.fetchone())
    r["start_time"] = datetime.fromisoformat(r["start_time"]) if r.get("start_time") else None
    r["end_time"] = datetime.fromisoformat(r["end_time"]) if r.get("end_time") else None
    if not r["end_time"]:
        raise HTTPException(status_code=400,detail="end_time is required")
    schedule_assignment_notifications(aid,r["end_time"].isoformat()) 
    return AssignmentRead(**r)

@router.get("/{project_id}/assignments",response_model = list[AssignmentRead])
async def read_assignments(project_id:int,db:sqlite3.Connection=Depends(get_db)):
    cur = db.cursor()
    cur.execute("""
    SELECT e.name as employee_name,ea.*
    FROM employees e
    LEFT JOIN employee_assignments ea ON e.id = ea.employee_id 
    WHERE ea.project_id = ?
    """, (project_id,))
    rows = cur.fetchall()
    Assignments_list = []
    for r in rows:
        assignmentread = AssignmentRead(
            id=r["id"],
            employee_name=r["employee_name"],
            employee_id=r["employee_id"],
            project_id=r["project_id"],
            start_time=datetime.fromisoformat(r["start_time"]),
            end_time=datetime.fromisoformat(r["end_time"]),
        )

        Assignments_list.append(assignmentread)
    return Assignments_list



@router.get("/{project_id}/members", response_model=list[dict])
def list_members(project_id: int, db: sqlite3.Connection = Depends(get_db)):
    """返回项目成员列表，格式近似文档中的 member: {id: name}。"""
    cur = db.cursor()
    cur.execute("SELECT id FROM projects WHERE id = ?", (project_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Project not found")
    cur.execute(
        """
        SELECT ea.employee_id as employee_id, e.name as name
        FROM employee_assignments ea
        JOIN employees e ON ea.employee_id = e.id
        WHERE ea.project_id = ?
        """,
        (project_id,),
    )
    rows = cur.fetchall()
    return [{"employee_id": r["employee_id"], "name": r["name"]} for r in rows]