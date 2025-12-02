from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.core.config import settings
from app.core.security import hash_password, verify_password, jwt_encode, jwt_decode
from sqlalchemy import select
from app.db.models import User


router = APIRouter(tags=["auth"], prefix="/auth")


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: Session = Depends(get_session)):
    obj = session.execute(select(User).where(User.username == payload.username)).scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(payload.password, obj.password_salt, obj.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt_encode({"sub": obj.id, "username": obj.username, "role": obj.role}, settings.SECRET_KEY, 3600 * 12)
    return TokenResponse(access_token=token, user={"id": obj.id, "username": obj.username, "role": obj.role})


@router.get("/me")
def me(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = auth.split(" ", 1)[1]
    try:
        payload = jwt_decode(token, settings.SECRET_KEY)
        return {"id": payload.get("sub"), "username": payload.get("username"), "role": payload.get("role")}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/logout")
def logout():
    # JWT 为无状态，前端删除本地令牌即可。
    return {"ok": True}
