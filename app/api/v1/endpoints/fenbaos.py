from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_fenbao_repo, IFenBaoRepository, get_fenbao_team_repo, IFenBaoTeamRepository
from app.schemas.fenbaos import FenBaoRead, FenBaoCreate, FenBaoUpdate, FenbaoTeam, FenbaoTeamRead, FenbaoTeamUpdate

router = APIRouter(tags=["fenbaos"],prefix="/fenbaos")

@router.get("/",response_model=list[FenBaoRead])
async def read_fenbaos(fenbao_repo: IFenBaoRepository = Depends(get_fenbao_repo)):
    return await fenbao_repo.read_all()

@router.post("/")
async def create_fenbao(payload:FenBaoCreate,fenbao_repo:IFenBaoRepository = Depends(get_fenbao_repo)):
    return await fenbao_repo.create(payload)

@router.put("/{fenbao_id}")
async def update_fenbao(fenbao_id:int,payload:FenBaoUpdate,fenbao_repo:IFenBaoRepository = Depends(get_fenbao_repo)):
    return await fenbao_repo.update(fenbao_id,payload)

@router.delete("/{fenbao_id}")
async def delete_fenbao(fenbao_id:int,fenbao_repo:IFenBaoRepository = Depends(get_fenbao_repo)):
    return await fenbao_repo.delete(fenbao_id)

@router.post("/teams")
async def create_team(payload: FenbaoTeam, repo: IFenBaoTeamRepository = Depends(get_fenbao_team_repo)):
    return await repo.assign_team(payload)

@router.get("/teams", response_model=list[FenbaoTeamRead])
async def list_teams(repo: IFenBaoTeamRepository = Depends(get_fenbao_team_repo)):
    return await repo.read_all()

@router.get("/teams/{team_id}", response_model=FenbaoTeamRead)
async def get_team(team_id: int, repo: IFenBaoTeamRepository = Depends(get_fenbao_team_repo)):
    return await repo.read_by_id(team_id)

@router.put("/teams/{team_id}", response_model=FenbaoTeamRead)
async def update_team(team_id: int, payload: FenbaoTeamUpdate, repo: IFenBaoTeamRepository = Depends(get_fenbao_team_repo)):
    return await repo.update(team_id, payload)

@router.delete("/teams/{team_id}")
async def delete_team(team_id: int, repo: IFenBaoTeamRepository = Depends(get_fenbao_team_repo)):
    return await repo.delete(team_id)

@router.post("/teams/{team_id}/complete")
async def complete_team(team_id: int, repo: IFenBaoTeamRepository = Depends(get_fenbao_team_repo)):
    return await repo.complete(team_id)

