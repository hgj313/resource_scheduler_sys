from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr

from app.dependencies import get_user_repo
from app.repositories.interfaces import IUserRepository
from app.core.security import jwt_decode
from app.core.config import settings

router = APIRouter(tags=["users"], prefix="/users")


class UserRead(BaseModel):
    id: int
    username: str
    role: str | None = None
    user_email: EmailStr | None = None

    class Config:
        from_attributes = True


@router.get("/me", response_model=UserRead)
async def get_user_me(request: Request, repo: IUserRepository = Depends(get_user_repo)):
    """获取当前登录用户的信息。"""
    auth = request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = auth.split(" ", 1)[1]
    try:
        payload = jwt_decode(token, settings.SECRET_KEY)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        d = await repo.read_by_id(user_id)
        return UserRead(**d)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, repo: IUserRepository = Depends(get_user_repo)):
    """根据用户ID获取用户信息。"""
    d = await repo.read_by_id(user_id)
    return UserRead(**d)
