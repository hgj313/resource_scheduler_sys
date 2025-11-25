from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
import sqlite3

from app.db.session import get_db
from app.core.config import settings
from app.core.security import hash_password, verify_password, jwt_encode, jwt_decode


router = APIRouter(tags=["auth"], prefix="/auth")


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT id, username, password_salt, password_hash, role FROM users WHERE username = ?", (payload.username,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = dict(row)
    if not verify_password(payload.password, user["password_salt"], user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt_encode({"sub": user["id"], "username": user["username"], "role": user.get("role")}, settings.SECRET_KEY, 3600 * 12)
    return TokenResponse(access_token=token, user={"id": user["id"], "username": user["username"], "role": user.get("role")})


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