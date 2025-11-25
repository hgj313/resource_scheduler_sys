from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from app.db.session import get_db
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeRead
from app.repositories.interfaces import IEmployeeAssignmentRepository
from app.schemas import AssignmentRead
from app.dependencies import get_assignment_repo

router = APIRouter(tags=["employees"], prefix="/employees")


@router.post("/", response_model=EmployeeRead)
async def create_employee(payload: EmployeeCreate, db: sqlite3.Connection = Depends(get_db)):
    """创建员工。"""
    cur = db.cursor()
    data = payload.model_dump()
    
    # 检查是否已存在相同姓名和邮箱的员工
    cur.execute(
        "SELECT * FROM employees WHERE name = ? AND email = ?",
        (data.get("name"), data.get("email"))
    )
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Employee with this name and email already exists")
    
    try:
        cur.execute(
            """
            INSERT INTO employees (name, gender, email, phone, position, department, region)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("name"),
                data.get("gender"),
                data.get("email"),
                data.get("phone"),
                data.get("position"),
                data.get("department"),
                data.get("region"),
            ),
        )
        db.commit()
        emp_id = cur.lastrowid
        cur.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
        row = cur.fetchone()
        return EmployeeRead(**dict(row))
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Employee with this name and email already exists")


@router.get("/", response_model=list[EmployeeRead])
async def list_employees(db: sqlite3.Connection = Depends(get_db)):
    """列出员工。"""
    cur = db.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    return [EmployeeRead(**dict(r)) for r in rows]


@router.get("/{employee_id}", response_model=EmployeeRead)
async def get_employee(employee_id: int, db: sqlite3.Connection = Depends(get_db)):
    """获取员工详情。"""
    cur = db.cursor()
    cur.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeRead(**dict(row))

@router.get("/{employee_id}/assignments", response_model=list[AssignmentRead])
async def get_employee_assignments(employee_id: int, assign_repo: IEmployeeAssignmentRepository = Depends(get_assignment_repo)):
    """获取员工所有任务分配记录。"""
    assignments = await assign_repo.read_by_employee_id(employee_id)
    return assignments
  

@router.put("/{employee_id}", response_model=EmployeeRead)
async def update_employee(employee_id: int, payload: EmployeeUpdate, db: sqlite3.Connection = Depends(get_db)):
    """更新员工信息。"""
    cur = db.cursor()
    cur.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Employee not found")
    updates = payload.model_dump(exclude_unset=True)
    if updates:
        set_clauses = []
        values = []
        for k, v in updates.items():
            set_clauses.append(f"{k} = ?")
            values.append(v)
        values.append(employee_id)
        sql = f"UPDATE employees SET {', '.join(set_clauses)} WHERE id = ?"
        cur.execute(sql, tuple(values))
        db.commit()
    cur.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    row = cur.fetchone()
    return EmployeeRead(**dict(row))


@router.delete("/{employee_id}")
async def delete_employee(employee_id: int, db: sqlite3.Connection = Depends(get_db)):
    """删除员工。"""
    cur = db.cursor()
    cur.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.commit()
    return {"deleted": True}