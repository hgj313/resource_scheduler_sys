from fastapi import Depends
from app.repositories.interfaces  import IEmployeeAssignmentRepository
from app.repositories.postgresql_repo import PostgresEmployeeAssignmentRepository
from app.repositories.interfaces  import IEmployeeRepository
from app.repositories.postgresql_repo import PostgresEmployeeRepository, PostgresRegionRepository, PostgresFilterRepository, PostgresProjectRepository, PostgresUserRepository
from app.repositories.interfaces  import IRegionRepository, IFilterRepository, IProjectRepository, IUserRepository
from app.service_repo.time_conflict_service import TimeConflictService
from app.db.session import get_session
from sqlalchemy.orm import Session
from app.core.config import settings

def get_assignment_repo(session: Session = Depends(get_session))->IEmployeeAssignmentRepository:
    return PostgresEmployeeAssignmentRepository(session=session)

def get_employee_repo(session: Session = Depends(get_session)) -> IEmployeeRepository:
    return PostgresEmployeeRepository(session=session)

def get_region_repo(session: Session = Depends(get_session)) -> IRegionRepository:
    return PostgresRegionRepository(session=session)

def get_filter_repo(session: Session = Depends(get_session)) -> IFilterRepository:
    return PostgresFilterRepository(session=session)

def get_project_repo(session: Session = Depends(get_session)) -> IProjectRepository:
    return PostgresProjectRepository(session=session)

def get_user_repo(session: Session = Depends(get_session)) -> IUserRepository:
    return PostgresUserRepository(session=session)

def get_time_conflict_service(assignment_repo: IEmployeeAssignmentRepository = Depends(get_assignment_repo)) -> TimeConflictService:
    return TimeConflictService(assignment_repo)
