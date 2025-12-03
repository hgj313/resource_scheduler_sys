from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_fenbao_repo, IFenBaoRepository
from app.schemas.fenbaos import FenBaoRead,FenBaoCreate,FenBaoUpdate

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