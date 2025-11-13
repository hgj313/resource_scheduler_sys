from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from app.db.session import get_db
from app.schemas import RegionCreate, RegionUpdate, RegionRead


router = APIRouter(tags=["regions"], prefix="/regions")


@router.post("/", response_model=RegionRead)
def create_region(payload: RegionCreate, db: sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()
    data = payload.model_dump()
    
    # 检查是否已存在同名区域
    cur.execute("SELECT * FROM regions WHERE name = ?", (data.get("name"),))
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Region with this name already exists")
    
    try:
        cur.execute(
            "INSERT INTO regions (name, location) VALUES (?, ?)",
            (data.get("name"), data.get("location")),
        )
        db.commit()
        rid = cur.lastrowid
        cur.execute("SELECT * FROM regions WHERE id = ?", (rid,))
        return RegionRead(**dict(cur.fetchone()))
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Region with this name already exists")


@router.get("/", response_model=list[RegionRead])
def list_regions(db: sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM regions")
    rows = cur.fetchall()
    return [RegionRead(**dict(r)) for r in rows]


@router.get("/{region_id}", response_model=RegionRead)
def get_region(region_id: int, db: sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM regions WHERE id = ?", (region_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Region not found")
    return RegionRead(**dict(row))


@router.put("/{region_id}", response_model=RegionRead)
def update_region(region_id: int, payload: RegionUpdate, db: sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM regions WHERE id = ?", (region_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Region not found")
    updates = payload.model_dump(exclude_unset=True)
    if updates:
        set_clauses = []
        values = []
        for k, v in updates.items():
            set_clauses.append(f"{k} = ?")
            values.append(v)
        values.append(region_id)
        sql = f"UPDATE regions SET {', '.join(set_clauses)} WHERE id = ?"
        cur.execute(sql, tuple(values))
        db.commit()
    cur.execute("SELECT * FROM regions WHERE id = ?", (region_id,))
    return RegionRead(**dict(cur.fetchone()))


@router.delete("/{region_id}")
def delete_region(region_id: int, db: sqlite3.Connection = Depends(get_db)):
    cur = db.cursor()
    cur.execute("DELETE FROM regions WHERE id = ?", (region_id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Region not found")
    db.commit()
    return {"deleted": True}