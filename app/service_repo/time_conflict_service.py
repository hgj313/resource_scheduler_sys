from datetime import datetime
from app.repositories.interfaces import IEmployeeAssignmentRepository

class TimeConflictService:
    def __init__(self,assign_repo:IEmployeeAssignmentRepository):
        self.assign_repo = assign_repo

    async def check_time_conflict(
        self,
        employee_id:int,
        start_time:datetime,
        end_time:datetime
        ):
        """检查指派时间段内，员工是否存在其他安排"""
        assignments = await self.assign_repo.read_by_employee_id(employee_id)
        conflict_list = []
        for assignment in assignments:
            max_start = max(assignment.start_time,start_time)
            min_end = min(assignment.end_time,end_time)
            if max_start < min_end:
                conflict = {
                    "id":assignment.id,
                    "project_id":assignment.project_id,
                    "conflict_start":str(max_start),
                    "conflict_end":str(min_end),
                }
                conflict_list.append(conflict)
        return conflict_list
