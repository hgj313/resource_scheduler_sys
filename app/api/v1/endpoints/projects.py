from datetime import datetime,timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.schemas import ProjectCreate, ProjectUpdate, ProjectRead, ProjectAssignCreate, AssignmentRead
from app.db.models import Project, Employee
from app.services.scheduler import schedule_assignment_notifications
from app.dependencies import get_time_conflict_service
from app.schemas.assignment import AssignmentUpdate
from app.repositories.interfaces import IEmployeeAssignmentRepository, IProjectRepository
from app.dependencies import get_assignment_repo, get_project_repo
from app.errorhandler.bussinesserror import TimeConflictError
from app.service_repo.time_conflict_service import TimeConflictService


router = APIRouter(tags=["projects"], prefix="/projects")


@router.post("/", response_model=ProjectRead)
async def create_project(payload: ProjectCreate, repo: IProjectRepository = Depends(get_project_repo)):
    return await repo.create(payload)


@router.get("/", response_model=list[ProjectRead])
async def list_projects(repo: IProjectRepository = Depends(get_project_repo)):
    return await repo.list()


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: int, repo: IProjectRepository = Depends(get_project_repo)):
    return await repo.get(project_id)


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(project_id: int, payload: ProjectUpdate, repo: IProjectRepository = Depends(get_project_repo)):
    return await repo.update(project_id, payload)


@router.delete("/{project_id}")
async def delete_project(project_id: int, repo: IProjectRepository = Depends(get_project_repo)):
    await repo.delete(project_id)
    return {"deleted": True}


@router.post("/{project_id}/assignments", response_model=AssignmentRead)
async def assign_employee(
    project_id: int, payload: ProjectAssignCreate,
    session: Session = Depends(get_session),
    tc: TimeConflictService = Depends(get_time_conflict_service),
    repo: IEmployeeAssignmentRepository = Depends(get_assignment_repo)
     ):
    """为项目指派员工及其时间段（拖曳分配的接口形态）。"""
    if not session.get(Project, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    if not session.get(Employee, payload.employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")

    if payload.end_time <= payload.start_time:
        raise HTTPException(status_code=400, detail="end_time must be greater than start_time")
    
    conflicts = await tc.check_time_conflict(payload.employee_id, payload.start_time, payload.end_time)
    if conflicts:
        raise TimeConflictError(conflicts)

    payload.project_id = project_id
    created = await repo.create(payload)
    if not created.end_time:
        raise HTTPException(status_code=400, detail="end_time is required")
    schedule_assignment_notifications(created.id, created.end_time.isoformat())
    return created

@router.put("/{project_id}/assignments/{assignment_id}",response_model=AssignmentRead)
async def update_assignment(
    project_id:int,
    assignment_id:int,
    payload:AssignmentUpdate,
    repo:IEmployeeAssignmentRepository = Depends(get_assignment_repo)
):
    return await repo.update(assignment_id,payload)

@router.get("/{project_id}/assignments",response_model = list[AssignmentRead])
async def read_assignments(project_id:int, repo: IEmployeeAssignmentRepository = Depends(get_assignment_repo)):
    return await repo.read_by_project_id(project_id)



@router.get("/{project_id}/members", response_model=list[dict])
async def list_members(project_id: int, repo: IEmployeeAssignmentRepository = Depends(get_assignment_repo)):
    """返回项目成员列表，格式近似文档中的 member: {id: name}。"""
    assignments = await repo.read_by_project_id(project_id)
    if not assignments:
        raise HTTPException(status_code=404, detail="Project not found")
    seen = {}
    out = []
    for a in assignments:
        if a.employee_id not in seen:
            seen[a.employee_id] = True
            out.append({"employee_id": a.employee_id, "name": a.employee_name})
    return out

@router.post("/{project_id}/fenbao")
async def create_fenbao_assignment(
    project_id:int,
    fenbao_id:int,
    repo:IProjectRepository = Depends(get_project_repo)
):
    return await repo.add_fenbao(project_id,fenbao_id)

@router.delete("/{project_id}/fenbao")
async def delete_fenbao_assignment(
    project_id:int,
    fenbao_id:int,
    repo:IProjectRepository = Depends(get_project_repo)
):
    return await repo.remove_fenbao(project_id,fenbao_id)
