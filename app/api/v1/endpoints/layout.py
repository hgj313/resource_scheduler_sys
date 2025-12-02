from fastapi import APIRouter, Depends, HTTPException,Body
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.db.models import Project
from app.repositories.interfaces import IEmployeeAssignmentRepository, IProjectRepository
from app.dependencies import get_assignment_repo, get_project_repo
from app.schemas.assignment import AssignmentRead
from app.services.sortlayout import sort_layout_user,sort_layout_project
from app.services.timeline import NewTimeDelta
from app.schemas.layouter import LayoutRead,LayoutProject,LayoutProjectRead

router = APIRouter(tags=["layout"],prefix="/layout")

@router.get("/{project_id}",response_model=list[LayoutRead])
async def get_layout_ratio(project_id:int, session: Session = Depends(get_session), repo: IEmployeeAssignmentRepository = Depends(get_assignment_repo)):
    rows = await repo.read_by_project_id(project_id)
    if not rows:
        raise HTTPException(status_code=404, detail="No layout found for this project")
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_range = NewTimeDelta(start_time = datetime.fromisoformat(project.start_time), end_time = datetime.fromisoformat(project.end_time))
    proportion_list = sort_layout_user(project_range,rows)
    return proportion_list

    
@router.post("/{region}",response_model=list[LayoutProjectRead])
async def get_layout_ratio(region:str|None = None,payload:LayoutProject=Body(...,description=" Contain project_id and main_timeline"), repo: IProjectRepository = Depends(get_project_repo)):
    main_start_time = payload.main_start_time
    main_end_time = payload.main_end_time
    main_range = NewTimeDelta(main_start_time,main_end_time)
    rows = await repo.list_by_ids_and_region(payload.project_id_list, region)
    if not rows:
        raise HTTPException(status_code=404, detail="Project not found")
    project_layout_ratio_list = []
    for row in rows:
        start_time = row.start_time
        end_time = row.end_time
        layout_range = NewTimeDelta(start_time,end_time)
        start_point_ratio,project_ratio = sort_layout_project(main_range,layout_range)
        layoutprojectread = LayoutProjectRead(
            project_id = row.id,
            project_name = row.name,
            start_point_ratio = start_point_ratio,
            project_ratio = project_ratio,
        )
        project_layout_ratio_list.append(layoutprojectread)
    return project_layout_ratio_list
    
