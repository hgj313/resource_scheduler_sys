from datetime import datetime
from app.repositories.interfaces import IEmployeeAssignmentRepository
from app.schemas.assignment import AssignmentUpdate
from app.schemas.project import ProjectAssignCreate
from sqlalchemy import select
from app.db.models import EmployeeAssignment


class TimeConflictService:
    def __init__(
        self,
        assign_repo:IEmployeeAssignmentRepository

        ):
        self.assign_repo = assign_repo

    async def check_time_conflict(
        self,
        employee_id:int,
        start_time:datetime,
        end_time:datetime
        ):
        assignments = await self.assign_repo.read_by_employee_id(employee_id)
        conflict_list = []
        for assignment in assignments:
            max_start = max(assignment.start_time, start_time)
            min_end = min(assignment.end_time, end_time)
            if max_start < min_end:
                conflict_list.append({
                    "id": assignment.id,
                    "project_id": assignment.project_id,
                    "conflict_start": max_start,
                    "conflict_end": min_end,
                })
        return conflict_list

    async def solve_time_conflict(
        self,
        employee_id:int,
        start_time:datetime,
        end_time:datetime,
        conflicts: list | None = None
        ):
        conflict_list = conflicts if conflicts is not None else await self.check_time_conflict(employee_id, start_time, end_time)
        if not conflict_list:
            return

        session = getattr(self.assign_repo, 'session', None)

        def _to_dt(v):
            from datetime import datetime as _dt
            return _dt.fromisoformat(v) if isinstance(v, str) else v

        if session is not None:
            with session.begin():
                for conflict in conflict_list:
                    session.execute(
                        select(EmployeeAssignment)
                        .where(EmployeeAssignment.id == conflict["id"]) 
                        .with_for_update()
                    )
                    current = await self.assign_repo.read_by_id(conflict["id"])
                    cs = conflict["conflict_start"]
                    ce = conflict["conflict_end"]
                    s = _to_dt(current.start_time)
                    e = _to_dt(current.end_time)
                    if s >= cs and e >= ce:
                        await self.assign_repo.update(conflict["id"], AssignmentUpdate(
                            employee_id=current.employee_id,
                            project_id=current.project_id,
                            start_time=ce,
                            end_time=e,
                        ))
                    elif s <= cs and e <= ce:
                        await self.assign_repo.update(conflict["id"], AssignmentUpdate(
                            employee_id=current.employee_id,
                            project_id=current.project_id,
                            start_time=s,
                            end_time=cs,
                        ))
                    elif s <= cs and e >= ce:
                        # 左段保留到 cs，右段新建从 ce 到原 e
                        await self.assign_repo.update(conflict["id"], AssignmentUpdate(
                            employee_id=current.employee_id,
                            project_id=current.project_id,
                            start_time=s,
                            end_time=cs,
                        ))
                        await self.assign_repo.create(ProjectAssignCreate(
                            employee_id=employee_id,
                            project_id=current.project_id,
                            start_time=ce,
                            end_time=e,
                        ))
        else:
            # 无 session 时退化为非锁定更新
            for conflict in conflict_list:
                current = await self.assign_repo.read_by_id(conflict["id"])
                cs = conflict["conflict_start"]
                ce = conflict["conflict_end"]
                s = _to_dt(current.start_time)
                e = _to_dt(current.end_time)
                if s >= cs and e >= ce:
                    await self.assign_repo.update(conflict["id"], AssignmentUpdate(
                        employee_id=current.employee_id,
                        project_id=current.project_id,
                        start_time=ce,
                        end_time=e,
                    ))
                elif s <= cs and e <= ce:
                    await self.assign_repo.update(conflict["id"], AssignmentUpdate(
                        employee_id=current.employee_id,
                        project_id=current.project_id,
                        start_time=s,
                        end_time=cs,
                    ))
                elif s <= cs and e >= ce:
                    await self.assign_repo.update(conflict["id"], AssignmentUpdate(
                        employee_id=current.employee_id,
                        project_id=current.project_id,
                        start_time=s,
                        end_time=cs,
                    ))
                    await self.assign_repo.create(EmployeeAssignmentCreate(
                        employee_id=employee_id,
                        project_id=current.project_id,
                        start_time=ce,
                        end_time=e,
                    ))
                    
