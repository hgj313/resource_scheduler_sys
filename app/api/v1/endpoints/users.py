from fastapi import APIRouter, Depends, HTTPException, Request
import sqlite3
from pydantic import BaseModel, EmailStr

from app.db.session import get_db
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
def get_user_me(request: Request, db: sqlite3.Connection = Depends(get_db)):
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
        
        cur = db.cursor()
        cur.execute(
            "SELECT id, username, role, user_email FROM users WHERE id = ?", 
            (user_id,)
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserRead(**dict(row))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    """根据用户ID获取用户信息。"""
    cur = db.cursor()
    cur.execute(
        "SELECT id, username, role, user_email FROM users WHERE id = ?", 
        (user_id,)
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserRead(**dict(row))