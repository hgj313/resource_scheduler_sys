from re import L
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import select, update, delete, func
from fastapi import Depends, HTTPException
from app.db.session import get_session
from app.db.models import EmployeeAssignment, Employee, Project, Region, User, FenBao, FenBaoTeam
from .interfaces import IEmployeeAssignmentRepository, IEmployeeRepository, IRegionRepository, IFilterRepository, IProjectRepository, IUserRepository,IFenBaoRepository,IFenBaoTeamRepository
from app.schemas import ProjectRead
from app.schemas.employee import EmployeeAssign
from app.services.timeline import NewTimeDelta, project_in_main_timeline, employee_available_in_secondary
from app.schemas.project import ProjectAssignCreate
from app.schemas.employee import EmployeeRead, EmployeeCreate, EmployeeUpdate
from app.schemas.assignment import AssignmentRead, AssignmentUpdate
from app.schemas.fenbaos import FenBaoRead, FenBaoCreate, FenBaoUpdate,FenbaoTeam,FenbaoTeamRead,FenbaoTeamUpdate
from typing import List

class PostgresEmployeeAssignmentRepository(IEmployeeAssignmentRepository):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def create(self, assignment: ProjectAssignCreate) -> AssignmentRead:
        obj = EmployeeAssignment(
            employee_id=assignment.employee_id,
            project_id=assignment.project_id,
            start_time=assignment.start_time.isoformat() if assignment.start_time else None,
            end_time=assignment.end_time.isoformat() if assignment.end_time else None,
            assigner_email=assignment.user_email,
        )
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return AssignmentRead(
            id=obj.id,
            employee_name=None,
            employee_id=obj.employee_id,
            project_id=obj.project_id,
            start_time=assignment.start_time,
            end_time=assignment.end_time,
        )
    async def read_by_id(self,assignment_id:int) ->AssignmentRead:
        assignment = self.session.get(EmployeeAssignment,assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        return AssignmentRead(
            id=assignment.id,
            employee_name=None,
            employee_id=assignment.employee_id,
            project_id=assignment.project_id,
            start_time=assignment.start_time,
            end_time=assignment.end_time,
        )
    async def read_by_employee_id(self, employee_id: int) -> list[AssignmentRead]:
        stmt = (
            select(EmployeeAssignment.id, EmployeeAssignment.employee_id, EmployeeAssignment.project_id,
                   EmployeeAssignment.start_time, EmployeeAssignment.end_time, Employee.name.label("employee_name"))
            .join(Employee, Employee.id == EmployeeAssignment.employee_id, isouter=True)
            .where(EmployeeAssignment.employee_id == employee_id)
        )
        rows = self.session.execute(stmt).all()
        results = []
        for r in rows:
            d = {
                "id": r.id,
                "employee_id": r.employee_id,
                "project_id": r.project_id,
                "start_time": None,
                "end_time": None,
                "employee_name": r.employee_name,
            }
            if r.start_time:
                from datetime import datetime
                d["start_time"] = datetime.fromisoformat(r.start_time)
            if r.end_time:
                from datetime import datetime
                d["end_time"] = datetime.fromisoformat(r.end_time)
            results.append(AssignmentRead(**d))
        return results

    async def read_by_project_id(self, project_id: int) -> list[AssignmentRead]:
        stmt = (
            select(EmployeeAssignment.id, EmployeeAssignment.employee_id, EmployeeAssignment.project_id,
                   EmployeeAssignment.start_time, EmployeeAssignment.end_time, Employee.name.label("employee_name"))
            .join(Employee, Employee.id == EmployeeAssignment.employee_id, isouter=True)
            .where(EmployeeAssignment.project_id == project_id)
        )
        rows = self.session.execute(stmt).all()
        results = []
        for r in rows:
            d = {
                "id": r.id,
                "employee_id": r.employee_id,
                "project_id": r.project_id,
                "start_time": None,
                "end_time": None,
                "employee_name": r.employee_name,
            }
            if r.start_time:
                from datetime import datetime
                d["start_time"] = datetime.fromisoformat(r.start_time)
            if r.end_time:
                from datetime import datetime
                d["end_time"] = datetime.fromisoformat(r.end_time)
            results.append(AssignmentRead(**d))
        return results

    async def update(self, assignment_id:int,assignment: AssignmentUpdate) -> AssignmentRead:
        values = {
            "employee_id": assignment.employee_id,
            "project_id": assignment.project_id,
            "start_time": assignment.start_time.isoformat() if assignment.start_time else None,
            "end_time": assignment.end_time.isoformat() if assignment.end_time else None,
        }
        stmt = update(EmployeeAssignment).where(EmployeeAssignment.id == assignment_id).values(**values)
        self.session.execute(stmt)
        self.session.commit()
        return await self.read_by_id(assignment_id)

    async def delete(self, assignment_id: int) -> None:
        stmt = delete(EmployeeAssignment).where(EmployeeAssignment.id == assignment_id)
        self.session.execute(stmt)
        self.session.commit()

class PostgresEmployeeRepository(IEmployeeRepository):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def create_employee(self, employee: EmployeeCreate) -> EmployeeRead:
        # 唯一性：name+email 组合
        from sqlalchemy import select
        exists_stmt = select(Employee).where(Employee.name == employee.name, Employee.email == employee.email)
        exists_obj = self.session.execute(exists_stmt).scalar_one_or_none()
        if exists_obj:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Employee with this name and email already exists")
        obj = Employee(
            name=employee.name,
            gender=employee.gender,
            email=employee.email,
            phone=employee.phone,
            position=employee.position,
            department=employee.department,
            region=employee.region,
        )
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return EmployeeRead(
            id=obj.id,
            name=obj.name,
            gender=obj.gender,
            email=obj.email,
            phone=obj.phone,
            position=obj.position,
            department=obj.department,
            region=obj.region,
        )

    async def list_employees(self) -> list[EmployeeRead]:
        from sqlalchemy import select
        rows = self.session.execute(select(Employee)).scalars().all()
        return [EmployeeRead(id=o.id, name=o.name, gender=o.gender, email=o.email, phone=o.phone, position=o.position, department=o.department, region=o.region) for o in rows]

    async def read_by_id(self, employee_id: int) -> EmployeeRead:
        obj = self.session.get(Employee, employee_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeRead(id=obj.id, name=obj.name, gender=obj.gender, email=obj.email, phone=obj.phone, position=obj.position, department=obj.department, region=obj.region)

    async def read_by_name(self, name: str) -> EmployeeRead:
        stmt = select(Employee).where(Employee.name == name)
        obj = self.session.execute(stmt).scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeRead(id=obj.id, name=obj.name, gender=obj.gender, email=obj.email, phone=obj.phone, position=obj.position, department=obj.department, region=obj.region)

    async def read_by_position(self, position: str) -> EmployeeRead:
        stmt = select(Employee).where(Employee.position == position)
        obj = self.session.execute(stmt).scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeRead(id=obj.id, name=obj.name, gender=obj.gender, email=obj.email, phone=obj.phone, position=obj.position, department=obj.department, region=obj.region)

    async def read_by_region(self, region: str) -> EmployeeRead:
        stmt = select(Employee).where(Employee.region == region)
        obj = self.session.execute(stmt).scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeRead(id=obj.id, name=obj.name, gender=obj.gender, email=obj.email, phone=obj.phone, position=obj.position, department=obj.department, region=obj.region)

    async def read_by_department(self, department: str) -> EmployeeRead:
        stmt = select(Employee).where(Employee.department == department)
        obj = self.session.execute(stmt).scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeRead(id=obj.id, name=obj.name, gender=obj.gender, email=obj.email, phone=obj.phone, position=obj.position, department=obj.department, region=obj.region)

    async def read_by_region_position(self, region: str, position: str) -> EmployeeRead:
        stmt = select(Employee).where(Employee.region == region, Employee.position == position)
        obj = self.session.execute(stmt).scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeRead(id=obj.id, name=obj.name, gender=obj.gender, email=obj.email, phone=obj.phone, position=obj.position, department=obj.department, region=obj.region)

    async def update_employee(self, employee_id: int, employee: EmployeeUpdate) -> EmployeeRead:
        values = {}
        if employee.name is not None:
            values["name"] = employee.name
        if employee.gender is not None:
            values["gender"] = employee.gender
        if employee.email is not None:
            values["email"] = employee.email
        if employee.phone is not None:
            values["phone"] = employee.phone
        if employee.position is not None:
            values["position"] = employee.position
        if employee.department is not None:
            values["department"] = employee.department
        if employee.region is not None:
            values["region"] = employee.region
        if values:
            stmt = update(Employee).where(Employee.id == employee_id).values(**values)
            self.session.execute(stmt)
            self.session.commit()
        return await self.read_by_id(employee_id)

    async def delete_employee(self, employee_id: int) -> None:
        stmt = delete(Employee).where(Employee.id == employee_id)
        res = self.session.execute(stmt)
        self.session.commit()



class PostgresFilterRepository(IFilterRepository):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def filter_projects(self, main_range: NewTimeDelta, region: str | None) -> list[ProjectRead]:
        from sqlalchemy import select
        stmt = select(Project)
        if region:
            stmt = stmt.where(Project.region == region)
        rows = self.session.execute(stmt).scalars().all()
        results: list[ProjectRead] = []
        for r in rows:
            if not (r.start_time and r.end_time):
                continue
            pj_range = NewTimeDelta(datetime.fromisoformat(r.start_time), datetime.fromisoformat(r.end_time))
            if project_in_main_timeline(pj_range, main_range):
                results.append(ProjectRead(id=r.id, name=r.name, value=r.value, region=r.region,
                                           start_time=datetime.fromisoformat(r.start_time),
                                           end_time=datetime.fromisoformat(r.end_time)))
        return results

    async def filter_employees(self, secondary_range: NewTimeDelta, region: str | None) -> list[EmployeeAssign]:
        from sqlalchemy import select
        stmt = select(Employee)
        if region:
            stmt = stmt.where(Employee.region == region)
        employees = self.session.execute(stmt).scalars().all()
        # get assignments for all employees
        emp_ids = [e.id for e in employees]
        assign_stmt = select(EmployeeAssignment).where(EmployeeAssignment.employee_id.in_(emp_ids)) if emp_ids else select(EmployeeAssignment)
        assigns = self.session.execute(assign_stmt).scalars().all()
        # group assignments by employee
        by_emp: dict[int, list[NewTimeDelta]] = {eid: [] for eid in emp_ids}
        for a in assigns:
            s = datetime.fromisoformat(a.start_time) if a.start_time else None
            e = datetime.fromisoformat(a.end_time) if a.end_time else None
            by_emp.setdefault(a.employee_id, []).append(NewTimeDelta(s, e))
        results: list[EmployeeAssign] = []
        for emp in employees:
            ranges = by_emp.get(emp.id, [])
            if employee_available_in_secondary(ranges, secondary_range):
                results.append(EmployeeAssign(id=emp.id, name=emp.name, gender=emp.gender, email=emp.email, phone=emp.phone, position=emp.position, department=emp.department, region=emp.region, assign_timeline=ranges))
        return results

class PostgresProjectRepository(IProjectRepository):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def create(self, payload) -> ProjectRead:
        from sqlalchemy import select
        d = payload.model_dump()
        stmt = select(Project).where(Project.name == d.get("name"), Project.value == d.get("value", 0.0))
        if self.session.execute(stmt).scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Project with this name and value already exists")
        obj = Project(
            name=d.get("name"),
            value=d.get("value", 0.0),
            region=d.get("region"),
            start_time=d.get("start_time").isoformat() if d.get("start_time") else None,
            end_time=d.get("end_time").isoformat() if d.get("end_time") else None,
        )
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        row = {
            "id": obj.id,
            "name": obj.name,
            "value": obj.value,
            "region": obj.region,
            "start_time": datetime.fromisoformat(obj.start_time) if obj.start_time else None,
            "end_time": datetime.fromisoformat(obj.end_time) if obj.end_time else None,
        }
        return ProjectRead(**row)

    async def list(self) -> list[ProjectRead]:
        from sqlalchemy import select
        rows = self.session.execute(select(Project)).scalars().all()
        out = []
        for r in rows:
            row = {
                "id": r.id,
                "name": r.name,
                "value": r.value,
                "region": r.region,
                "start_time": datetime.fromisoformat(r.start_time) if r.start_time else None,
                "end_time": datetime.fromisoformat(r.end_time) if r.end_time else None,
            }
            out.append(ProjectRead(**row))
        return out

    async def get(self, project_id: int) -> ProjectRead:
        obj = self.session.get(Project, project_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Project not found")
        row = {
            "id": obj.id,
            "name": obj.name,
            "value": obj.value,
            "region": obj.region,
            "start_time": datetime.fromisoformat(obj.start_time) if obj.start_time else None,
            "end_time": datetime.fromisoformat(obj.end_time) if obj.end_time else None,
        }
        return ProjectRead(**row)

    async def update(self, project_id: int, payload) -> ProjectRead:
        obj = self.session.get(Project, project_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Project not found")
        updates = payload.model_dump(exclude_unset=True)
        for k, v in updates.items():
            if k in ("start_time", "end_time") and v is not None:
                v = v.isoformat()
            setattr(obj, k, v)
        self.session.commit()
        self.session.refresh(obj)
        return await self.get(project_id)

    async def delete(self, project_id: int) -> None:
        from sqlalchemy import delete
        stmt = delete(Project).where(Project.id == project_id)
        res = self.session.execute(stmt)
        self.session.commit()

    async def list_by_ids_and_region(self, ids: List[int], region: str | None) -> List[ProjectRead]:
        from sqlalchemy import select
        stmt = select(Project).where(Project.id.in_(ids))
        if region and region != "all":
            stmt = stmt.where(Project.region == region)
        rows = self.session.execute(stmt).scalars().all()
        out = []
        for r in rows:
            start = datetime.fromisoformat(r.start_time) if r.start_time else None
            end = datetime.fromisoformat(r.end_time) if r.end_time else None
            out.append(ProjectRead(id=r.id, name=r.name, value=r.value, region=r.region, start_time=start, end_time=end))
        return out

    async def add_fenbao(self, project_id: int, fenbao_id: int,assign_staff_counts:int) -> dict[str, str]:
        from sqlalchemy.exc import IntegrityError
        p = self.session.get(Project, project_id)
        if not p:
            raise HTTPException(status_code=404, detail="Project not found")
        f = self.session.get(FenBao, fenbao_id)
        if not f:
            raise HTTPException(status_code=404, detail="FenBao not found")
        if f.staff_count < assign_staff_counts:
            raise HTTPException(status_code=400, detail="FenBao staff count is not enough")
        try:
            p.fenbaos.append(f)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Relation already exists")
        return {"message":"FenBao added to project successfully"}
    
    async def remove_fenbao(self, project_id: int, fenbao_id: int) -> List[FenBaoRead]:
        p = self.session.get(Project, project_id)
        if not p:
            raise HTTPException(status_code=404, detail="Project not found")
        f = self.session.get(FenBao, fenbao_id)
        if not f:
            raise HTTPException(status_code=404, detail="FenBao not found")
        try:
            p.fenbaos.remove(f)
            self.session.commit()
        except ValueError:
            self.session.rollback()
            raise HTTPException(status_code=404, detail="Relation not found")
        out = []
        for x in p.fenbaos:
            out.append(FenBaoRead(id=x.id, name=x.name, professional=x.professional, staff_count=x.staff_count, level=x.level))
        return out

    async def read_all_fenbaos(self, project_id: int) -> List[FenBaoRead]:
        p = self.session.get(Project, project_id)
        if not p:
            raise HTTPException(status_code=404, detail="Project not found")
        out = []
        for x in p.fenbaos:
            out.append(FenBaoRead(id=x.id, name=x.name, professional=x.professional, staff_count=x.staff_count, level=x.level))
        return out

    async def list_projects_by_fenbao(self, fenbao_id: int) -> List[ProjectRead]:
        f = self.session.get(FenBao, fenbao_id)
        if not f:
            raise HTTPException(status_code=404, detail="FenBao not found")
        out = []
        for p in f.projects:
            start = datetime.fromisoformat(p.start_time) if p.start_time else None
            end = datetime.fromisoformat(p.end_time) if p.end_time else None
            out.append(ProjectRead(id=p.id, name=p.name, value=p.value, region=p.region, start_time=start, end_time=end))
        return out

class PostgresRegionRepository(IRegionRepository):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def create(self, name: str, location: str | None) -> dict:
        from sqlalchemy import select
        exists_stmt = select(Region).where(Region.name == name)
        if self.session.execute(exists_stmt).scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Region with this name already exists")
        obj = Region(name=name, location=location)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return {"id": obj.id, "name": obj.name, "location": obj.location}

    async def list(self) -> list[dict]:
        from sqlalchemy import select
        rows = self.session.execute(select(Region)).scalars().all()
        return [{"id": r.id, "name": r.name, "location": r.location} for r in rows]

    async def get(self, region_id: int) -> dict:
        obj = self.session.get(Region, region_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Region not found")
        return {"id": obj.id, "name": obj.name, "location": obj.location}

    async def update(self, region_id: int, updates: dict) -> dict:
        from sqlalchemy import update
        if updates:
            stmt = update(Region).where(Region.id == region_id).values(**updates)
            self.session.execute(stmt)
            self.session.commit()
        return await self.get(region_id)

    async def delete(self, region_id: int) -> None:
        from sqlalchemy import delete
        stmt = delete(Region).where(Region.id == region_id)
        res = self.session.execute(stmt)
        self.session.commit()

    async def get_employee_counts(self, region:str, repo: IEmployeeRepository = PostgresEmployeeRepository(session=get_session())) -> dict:
        stmt = select(func.count(Employee.id)).where(Employee.region == region)
        stmt2 = select(func.count(Employee.id)).where(Employee.region == region,Employee.position == "项目经理")
        stmt3 = select(func.count(Employee.id)).where(Employee.region == region,Employee.position == "硬景工程师")
        stmt4 = select(func.count(Employee.id)).where(Employee.region == region,Employee.position == "软景工程师")
        total_employees = self.session.execute(stmt).scalar_one()
        pm_count = self.session.execute(stmt2).scalar_one()
        hardscape_engineer_count = self.session.execute(stmt3).scalar_one()
        softscape_engineer_count = self.session.execute(stmt4).scalar_one()
        return {
            "total_employees": total_employees,
            "pm_count": pm_count,
            "hardscape_engineer_count": hardscape_engineer_count,
            "softscape_engineer_count": softscape_engineer_count,
        }



    async def get_project_counts(self, region: str, repo: IProjectRepository = PostgresProjectRepository(session=get_session())) -> int:
        stmt = select(func.count(Project.id)).where(Project.region == region)
        return self.session.execute(stmt).scalar_one()
        

class PostgresUserRepository(IUserRepository):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def read_by_id(self, user_id: int) -> dict:
        obj = self.session.get(User, user_id)
        if not obj:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": obj.id, "username": obj.username, "role": obj.role, "user_email": obj.user_email}

    async def read_by_position(self, position: str) -> EmployeeRead:
        stmt = select(Employee).where(Employee.position == position)
        obj = self.session.execute(stmt).scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeRead(
            id=obj.id,
            name=obj.name,
            gender=obj.gender,
            email=obj.email,
            phone=obj.phone,
            position=obj.position,
            department=obj.department,
            region=obj.region,
        )

    async def read_by_region(self, region: str) -> EmployeeRead:
        stmt = select(Employee).where(Employee.region == region)
        obj = self.session.execute(stmt).scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeRead(
            id=obj.id,
            name=obj.name,
            gender=obj.gender,
            email=obj.email,
            phone=obj.phone,
            position=obj.position,
            department=obj.department,
            region=obj.region,
        )

    async def read_by_department(self, department: str) -> EmployeeRead:
        stmt = select(Employee).where(Employee.department == department)
        obj = self.session.execute(stmt).scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeRead(
            id=obj.id,
            name=obj.name,
            gender=obj.gender,
            email=obj.email,
            phone=obj.phone,
            position=obj.position,
            department=obj.department,
            region=obj.region,
        )

    async def read_by_region_position(self, region: str, position: str) -> EmployeeRead:
        stmt = select(Employee).where(Employee.region == region, Employee.position == position)
        obj = self.session.execute(stmt).scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeRead(
            id=obj.id,
            name=obj.name,
            gender=obj.gender,
            email=obj.email,
            phone=obj.phone,
            position=obj.position,
            department=obj.department,
            region=obj.region,
        )

    async def update_employee(self, employee_id: int, employee: EmployeeUpdate) -> EmployeeRead:
        values = {}
        if employee.name is not None:
            values["name"] = employee.name
        if employee.gender is not None:
            values["gender"] = employee.gender
        if employee.email is not None:
            values["email"] = employee.email
        if employee.phone is not None:
            values["phone"] = employee.phone
        if employee.position is not None:
            values["position"] = employee.position
        if employee.department is not None:
            values["department"] = employee.department
        if employee.region is not None:
            values["region"] = employee.region
        if values:
            stmt = update(Employee).where(Employee.id == employee_id).values(**values)
            self.session.execute(stmt)
            self.session.commit()
        return await self.read_by_id(employee_id)

    async def delete_employee(self, employee_id: int) -> None:
        stmt = delete(Employee).where(Employee.id == employee_id)
        self.session.execute(stmt)
        self.session.commit()

class PostgresFenBaoRepository(IFenBaoRepository):
    def __init__(self,session:Session = Depends(get_session)):
        self.session = session
    
    async def create(self,fenbao:FenBaoCreate)->dict:
        """创建一个新的分包"""
        f = self.session.execute(select(FenBao).where(FenBao.name == fenbao.name)).scalar_one_or_none()
        if f:
            raise HTTPException(status_code=400,detail="FenBao name already exists")
        f = FenBao(**fenbao.model_dump())
        f.available_staff_count = fenbao.staff_count
        self.session.add(f)
        self.session.commit()
        return {"message":"FenBao created successfully"}


    async def read_by_id(self,fenbao_id:int)->FenBaoRead:
        """根据分包ID读取分包信息"""
        f = self.session.get(FenBao,fenbao_id)
        if not f:
            raise HTTPException(status_code=404,detail="FenBao not found")
        return FenBaoRead.model_validate(f)

    async def read_by_name(self,name:str)->FenBaoRead:
        """根据分包名称读取分包信息"""
        stmt = select(FenBao).where(FenBao.name == name)
        f = self.session.execute(stmt).scalar_one_or_none()
        if not f:
            raise HTTPException(status_code=404,detail="FenBao not found")
        return FenBaoRead.model_validate(f)

    async def read_by_professional(self,professional:str)->FenBaoRead:
        """根据专业读取分包信息"""
        stmt = select(FenBao).where(FenBao.professional == professional)
        f = self.session.execute(stmt).scalar_one_or_none()
        if not f:
            raise HTTPException(status_code=404,detail="FenBao not found")
        return FenBaoRead.model_validate(f)

    async def read_all(self)->List[FenBaoRead]:
        """列出所有分包"""
        
        stmt1 = select(FenBao).limit(1)
        fenbao = self.session.execute(stmt1).scalar_one_or_none()
        if not fenbao:
            raise HTTPException(status_code=404,detail="FenBao not found")
        stmt2 = select(FenBao)
        fens = self.session.execute(stmt2).scalars().all()
        return [FenBaoRead.model_validate(f) for f in fens]

    async def update(self,fenbao_id:int,fenbao:FenBaoUpdate)->FenBaoRead:
        """更新一个分包"""
        f = self.session.get(FenBao,fenbao_id)
        if not f:
            raise HTTPException(status_code=404,detail="FenBao not found")
        values = {}
        if fenbao.name is not None:
            values["name"] = fenbao.name
        if fenbao.professional is not None:
            values["professional"] = fenbao.professional
        if fenbao.staff_count is not None:
            values["staff_count"] = fenbao.staff_count
        if fenbao.available_staff_count is not None:
            values["available_staff_count"] = fenbao.available_staff_count
        if fenbao.level is not None:
            values["level"] = fenbao.level
        if values:
            stmt = update(FenBao).where(FenBao.id == fenbao_id).values(**values)
            self.session.execute(stmt)
            self.session.commit()
        return await self.read_by_id(fenbao_id)

    async def delete(self,fenbao_id:int)->dict:
        """删除一个分包"""
        f = self.session.get(FenBao,fenbao_id)
        if not f:
            raise HTTPException(status_code=404,detail="FenBao not found")
        stmt = delete(FenBao).where(FenBao.id == fenbao_id)
        self.session.execute(stmt)
        self.session.commit()
        return {"message":"Fenbao delete seccessfully"}
