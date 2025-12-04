from datetime import datetime
from app.repositories.interfaces import IFenBaoTeamRepository
from app.schemas.fenbaos import FenbaoTeamRead
class TimeConflictService:
    def __init__(self,fb_team_repo:IFenBaoTeamRepository):
        self.fb_team_repo = fb_team_repo

    async def check_time_conflict(
        self,
        team_id:int,
        start_time:datetime,
        end_time:datetime
        ):
        """检查指派时间段内，分包团队是否存在其他安排"""
        assignment = await self.fb_team_repo.read_by_id(team_id)
        max_start = max(assignment.start_time,start_time)
        min_end = min(assignment.end_time,end_time)
        if max_start < min_end:
            conflict = {
                "id":assignment.id,
                "project_id":assignment.project_id,
                "conflict_start":str(max_start),
                "conflict_end":str(min_end),
            }
        return conflict
