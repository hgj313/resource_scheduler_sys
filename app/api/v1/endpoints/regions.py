from fastapi import APIRouter, Depends, HTTPException
from app.schemas import RegionCreate, RegionUpdate, RegionRead
from app.repositories.interfaces import IRegionRepository
from app.dependencies import get_region_repo


router = APIRouter(tags=["regions"], prefix="/regions")


@router.post("/", response_model=RegionRead)
async def create_region(payload: RegionCreate, repo: IRegionRepository = Depends(get_region_repo)):
    data = payload.model_dump()
    r = await repo.create(data.get("name"), data.get("location"))
    return RegionRead(**r)


@router.get("/", response_model=list[RegionRead])
async def list_regions(repo: IRegionRepository = Depends(get_region_repo)):
    rows = await repo.list()
    return [RegionRead(**r) for r in rows]


@router.get("/{region_id}", response_model=RegionRead)
async def get_region(region_id: int, repo: IRegionRepository = Depends(get_region_repo)):
    row = await repo.get(region_id)
    return RegionRead(**row)


@router.put("/{region_id}", response_model=RegionRead)
async def update_region(region_id: int, payload: RegionUpdate, repo: IRegionRepository = Depends(get_region_repo)):
    updates = payload.model_dump(exclude_unset=True)
    row = await repo.update(region_id, updates)
    return RegionRead(**row)


@router.delete("/{region_id}")
async def delete_region(region_id: int, repo: IRegionRepository = Depends(get_region_repo)):
    await repo.delete(region_id)
    return {"deleted": True}
