from datetime import datetime
from app.core.config import settings
from app.core.security import hash_password
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, User


# SQLAlchemy 会话
_engine = create_engine(
    settings.DATABASE_URL,
    future=True,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=_engine)
    db = SessionLocal()
    try:
        from sqlalchemy import select
        cnt = db.execute(select(User).limit(1)).scalar_one_or_none()
        if not cnt:
            salt, pwd_hash = hash_password("admin123")
            db.add(User(username="admin", password_salt=salt, password_hash=pwd_hash, role="admin", user_email="3021922280@qq.com"))
            db.commit()
    except Exception:
        pass
    finally:
        db.close()


 # 已移除基于 sqlite3 的手动连接依赖
