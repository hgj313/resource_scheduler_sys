from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeRead
from app.repositories.interfaces import IEmployeeAssignmentRepository, IEmployeeRepository
from app.schemas import AssignmentRead
from app.dependencies import get_assignment_repo, get_employee_repo

router = APIRouter(tags=["employees"], prefix="/employees")


@router.post("/", response_model=EmployeeRead)
async def create_employee(payload: EmployeeCreate, repo: IEmployeeRepository = Depends(get_employee_repo)):
    """创建员工。"""
    return await repo.create_employee(payload)


@router.get("/", response_model=list[EmployeeRead])
async def list_employees(repo: IEmployeeRepository = Depends(get_employee_repo)):
    """列出员工。"""
    return await repo.list_employees()


@router.get("/{employee_id}", response_model=EmployeeRead)
async def get_employee(employee_id: int, repo: IEmployeeRepository = Depends(get_employee_repo)):
    """获取员工详情。"""
    return await repo.read_by_id(employee_id)

@router.get("/{employee_id}/assignments", response_model=list[AssignmentRead])
async def get_employee_assignments(employee_id: int, assign_repo: IEmployeeAssignmentRepository = Depends(get_assignment_repo)):
    """获取员工所有任务分配记录。"""
    assignments = await assign_repo.read_by_employee_id(employee_id)
    return assignments
  

@router.put("/{employee_id}", response_model=EmployeeRead)
async def update_employee(employee_id: int, payload: EmployeeUpdate, repo: IEmployeeRepository = Depends(get_employee_repo)):
    """更新员工信息。"""
    return await repo.update_employee(employee_id, payload)


@router.delete("/{employee_id}")
async def delete_employee(employee_id: int, repo: IEmployeeRepository = Depends(get_employee_repo)):
    """删除员工。"""
    await repo.delete_employee(employee_id)
    return {"deleted": True}
