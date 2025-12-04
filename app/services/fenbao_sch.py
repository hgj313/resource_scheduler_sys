from sqlalchemy import select, update
from sqlalchemy.orm import Session
from datetime import datetime

from fastapi import HTTPException
from typing import List
from app.repositories.interfaces import IFenBaoRepository, IFenBaoTeamRepository, IProjectRepository
from app.schemas.fenbaos import FenBaoUpdate, FenbaoTeam, FenbaoTeamRead, FenbaoTeamUpdate
from app.db.models import FenBaoTeam, Project
 

class PostgresFenBaoTeamRepository(IFenBaoTeamRepository):
    def __init__(self, session: Session, fb_repo: IFenBaoRepository | None = None):
        self.session = session
        self.fb_repo = fb_repo
    
    async def assign_team(
        self,
        team: FenbaoTeam,
        ) -> dict:
        """创建并派遣一个新的分包团队，并减少分包可用人数。"""
        exists = self.session.execute(
            select(FenBaoTeam).where(FenBaoTeam.leader_name == team.leader_name)
        ).scalar_one_or_none()
        if exists:
            raise HTTPException(status_code=400, detail="FenbaoTeam leader_name already exists")
        proj = self.session.get(Project, team.project_at_id)
        if not proj:
            raise HTTPException(status_code=400, detail="Project not found for project_at_id")
        payload = team.model_dump()
        if payload.get("start_time") is not None:
            payload["start_time"] = payload["start_time"].isoformat()
        if payload.get("end_time") is not None:
            payload["end_time"] = payload["end_time"].isoformat()
        t = FenBaoTeam(**payload)
        self.session.add(t)
        self.session.commit()
        fb_repo = self.fb_repo
        if fb_repo is None:
            raise HTTPException(status_code=500, detail="FenBaoRepository not provided")
        fb = await fb_repo.read_by_id(team.belong_to_fenbao_id)
        available = (fb.available_staff_count if fb.available_staff_count is not None else fb.staff_count)
        fb_staff_counts = available - (team.team_number or 0)
        if fb_staff_counts < 0:
            raise HTTPException(status_code=400, detail="FenBao available staff insufficient")
        await fb_repo.update(fb.id, FenBaoUpdate(available_staff_count=fb_staff_counts))
        return {"message": "FenbaoTeam assigned to project successfully"}
    
    async def read_by_id(
        self,
        team_id:int,
        )->FenbaoTeamRead:
        """根据分包团队ID读取团队信息"""
        t = self.session.execute(select(FenBaoTeam).where(FenBaoTeam.id == team_id)).scalar_one_or_none()
        if not t:
            raise HTTPException(status_code=404,detail="FenbaoTeam not found")
        project_name = self.session.execute(select(Project.name).where(Project.id == t.project_at_id)).scalar_one_or_none()
        s = t.start_time
        e = t.end_time
        try:
            start_dt = datetime.fromisoformat(s) if s else None
        except Exception:
            s2 = s.replace(" ", "T") if s else s
            s2 = (s2 + ":00") if (s2 and s2.endswith("+08")) else s2
            start_dt = datetime.fromisoformat(s2) if s2 else None
        try:
            end_dt = datetime.fromisoformat(e) if e else None
        except Exception:
            e2 = e.replace(" ", "T") if e else e
            e2 = (e2 + ":00") if (e2 and e2.endswith("+08")) else e2
            end_dt = datetime.fromisoformat(e2) if e2 else None
        if start_dt is None:
            raise HTTPException(status_code=400, detail="Invalid start_time format")
        return FenbaoTeamRead(
            id=t.id,
            leader_name=t.leader_name,
            company_name=t.company_name,
            team_number=t.team_number,
            project_at_id=t.project_at_id,
            start_time=start_dt,
            end_time=end_dt,
            level=t.level,
            belong_to_fenbao_id=t.belong_to_fenbao_id,
            status=t.status,
            project_name=project_name,
        )

    async def read_by_name(self,name:str)->FenbaoTeamRead:
        """根据分包名称读取分包团队信息"""
        t = self.session.execute(select(FenBaoTeam).where(FenBaoTeam.name == name)).scalar_one_or_none()
        if not t:
            raise HTTPException(status_code=404,detail="FenbaoTeam not found")
        return FenbaoTeamRead.model_validate(t)

    async def read_all(self)->List[FenbaoTeamRead]:
        """列出所有分包团队"""
        teams = self.session.execute(select(FenBaoTeam)).scalars().all()
        out: List[FenbaoTeamRead] = []
        for t in teams:
            s = t.start_time
            e = t.end_time
            try:
                start_dt = datetime.fromisoformat(s) if s else None
            except Exception:
                s2 = s.replace(" ", "T") if s else s
                s2 = (s2 + ":00") if (s2 and s2.endswith("+08")) else s2
                start_dt = datetime.fromisoformat(s2) if s2 else None
            try:
                end_dt = datetime.fromisoformat(e) if e else None
            except Exception:
                e2 = e.replace(" ", "T") if e else e
                e2 = (e2 + ":00") if (e2 and e2.endswith("+08")) else e2
                end_dt = datetime.fromisoformat(e2) if e2 else None
            if start_dt is None:
                continue
            out.append(FenbaoTeamRead(
                id=t.id,
                leader_name=t.leader_name,
                company_name=t.company_name,
                team_number=t.team_number,
                project_at_id=t.project_at_id,
                start_time=start_dt,
                end_time=end_dt,
                level=t.level,
                belong_to_fenbao_id=t.belong_to_fenbao_id,
                status=t.status,
                project_name=None,
            ))
        return out

    async def read_by_project_id(self, project_id:int)->List[FenbaoTeamRead]:
        teams = self.session.execute(select(FenBaoTeam).where(FenBaoTeam.project_at_id == project_id)).scalars().all()
        out: List[FenbaoTeamRead] = []
        for t in teams:
            s = t.start_time
            e = t.end_time
            try:
                start_dt = datetime.fromisoformat(s) if s else None
            except Exception:
                s2 = s.replace(" ", "T") if s else s
                s2 = (s2 + ":00") if (s2 and s2.endswith("+08")) else s2
                start_dt = datetime.fromisoformat(s2) if s2 else None
            try:
                end_dt = datetime.fromisoformat(e) if e else None
            except Exception:
                e2 = e.replace(" ", "T") if e else e
                e2 = (e2 + ":00") if (e2 and e2.endswith("+08")) else e2
                end_dt = datetime.fromisoformat(e2) if e2 else None
            if start_dt is None:
                continue
            out.append(FenbaoTeamRead(
                id=t.id,
                leader_name=t.leader_name,
                company_name=t.company_name,
                team_number=t.team_number,
                project_at_id=t.project_at_id,
                start_time=start_dt,
                end_time=end_dt,
                level=t.level,
                belong_to_fenbao_id=t.belong_to_fenbao_id,
                status=t.status,
                project_name=None,
            ))
        return out

    async def update(self,team_id:int,team:FenbaoTeamUpdate)->FenbaoTeamRead:
        """更新一个分包团队"""
        changes = team.model_dump(exclude_unset=True)
        if not changes:
            raise HTTPException(status_code=400,detail="No changes provided")
        t = self.session.execute(select(FenBaoTeam).where(FenBaoTeam.id == team_id)).scalar_one_or_none()
        if not t:
            raise HTTPException(status_code=404,detail="FenbaoTeam not found")
        if "project_at_id" in changes:
            proj = self.session.get(Project, changes["project_at_id"])
            if not proj:
                raise HTTPException(status_code=400, detail="Project not found for project_at_id")
        for k, v in list(changes.items()):
            if k in ("start_time", "end_time") and v is not None:
                changes[k] = v.isoformat()
        self.session.execute(
            update(FenBaoTeam)
            .where(FenBaoTeam.id == team_id)
            .values(**changes)
        )
        self.session.commit()
        t_now = await self.read_by_id(team_id)
        return t_now

    async def delete(self,team_id:int)->dict:
        """删除一个分包团队"""
        t = self.session.execute(select(FenBaoTeam).where(FenBaoTeam.id == team_id)).scalar_one_or_none()
        if not t:
            raise HTTPException(status_code=404,detail="FenbaoTeam not found")
        self.session.delete(t)
        self.session.commit()
        return {"message":"FenbaoTeam deleted successfully"}

    async def complete(self, team_id: int) -> dict:
        t = self.session.execute(select(FenBaoTeam).where(FenBaoTeam.id == team_id)).scalar_one_or_none()
        if not t:
            raise HTTPException(status_code=404, detail="FenbaoTeam not found")
        if t.status == "completed":
            return {"message": "FenbaoTeam already completed"}
        fb_repo = self.fb_repo
        if fb_repo is None:
            raise HTTPException(status_code=500, detail="FenBaoRepository not provided")
        fb = await fb_repo.read_by_id(t.belong_to_fenbao_id)
        available = (fb.available_staff_count if fb.available_staff_count is not None else fb.staff_count)
        restored = available + (t.team_number or 0)
        await fb_repo.update(fb.id, FenBaoUpdate(available_staff_count=restored))
        self.session.execute(
            update(FenBaoTeam).where(FenBaoTeam.id == team_id).values(status="completed")
        )
        self.session.commit()
        return {"message": "FenbaoTeam completed and availability restored"}
