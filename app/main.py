from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import init_db
from app.api.v1.endpoints.employees import router as employees_router
from app.api.v1.endpoints.projects import router as projects_router
from app.api.v1.endpoints.regions import router as regions_router
from app.api.v1.endpoints.filters import router as filters_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理：替代 @app.on_event。

    - 在 yield 之前执行启动逻辑（例如初始化数据库）
    - 在 yield 之后执行关闭清理（目前无）
    """
    init_db()
    yield


def create_app() -> FastAPI:
    """
    创建并配置 FastAPI 应用。

    - 加载配置
    - 注册路由
    """
    app = FastAPI(title="HRC 人力资源调度系统后端", version="0.1.0", lifespan=lifespan)

    # 注册路由到 /api/v1
    app.include_router(employees_router, prefix="/api/v1")
    app.include_router(projects_router, prefix="/api/v1")
    app.include_router(regions_router, prefix="/api/v1")
    app.include_router(filters_router, prefix="/api/v1")

    @app.get("/healthz", tags=["health"])
    def health_check():
        return {"status": "ok", "database_url": settings.DATABASE_URL}

    return app


app = create_app()