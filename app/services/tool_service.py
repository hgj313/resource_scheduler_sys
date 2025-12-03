from fastapi import Depends
from sqlalchemy.orm import Session
from app.repositories.interfaces  import IEmployeeRepository, IProjectRepository

from sqlalchemy import select, func
from app.db.models import Employee, Project, Region
from app.dependencies import get_employee_repo,get_project_repo
    
    
    
async def get_employee_counts(region_id: int, repo: IEmployeeRepository = Depends(get_employee_repo)) -> int:
        stmt = (
            select(func.count(Employee.id))
            .join(Region, Employee.region == Region.name)
            .where(Region.id == region_id)
        )
        return repo.session.execute(stmt).scalar_one()



async def get_project_counts(region_id: int, repo: IProjectRepository = Depends(get_project_repo)) -> int:
        stmt = (
            select(func.count(Project.id))
            .join(Region, Project.region == Region.name)
            .where(Region.id == region_id)
        )
        return repo.session.execute(stmt).scalar_one()
